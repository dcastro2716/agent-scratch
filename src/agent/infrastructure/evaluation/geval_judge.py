from typing import Annotated, Protocol

from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from agent.domain.evaluation import Verdict
from agent.domain.knowledge import Citation, SearchHit
from agent.domain.models import Message, Usage


GEVAL_PROMPT = """Evalúa la respuesta de un asistente bancario usando los fragmentos que recibió.

Califica cada criterio de 1 a 5:
- groundedness: 5 si todos los hechos están respaldados, 3 si solo lo está la mitad,
  1 si la respuesta inventa o contradice lo que dicen los fragmentos.
- relevance: 5 si responde exactamente a la pregunta, 1 si no la responde.
- citation_correct: 5 si las fuentes citadas respaldan las afirmaciones,
  1 si no las respaldan o no se citó ninguna.

Lee la pregunta y separa la respuesta en afirmaciones. Contrasta cada afirmación
con los fragmentos y comprueba si las fuentes citadas la respaldan. Explica tu
evaluación en dos o tres frases antes de indicar las puntuaciones."""


def _one_to_five(value: int) -> int:
    if not 1 <= value <= 5:
        raise ValueError("el puntaje va de 1 a 5")
    return value


Score = Annotated[int, AfterValidator(_one_to_five)]


class GEvalScores(BaseModel):
    """Respuesta estructurada del juez, con la explicación antes de las notas."""

    model_config = ConfigDict(extra="forbid")

    reasoning: str = Field(description="Justificación de las notas en dos o tres frases.")
    groundedness: Score = Field(description="De 1 a 5: respaldo de las afirmaciones en los fragmentos.")
    relevance: Score = Field(description="De 1 a 5: qué tan bien responde a la pregunta.")
    citation_correct: Score = Field(description="De 1 a 5: respaldo de las afirmaciones en las fuentes citadas.")


class StructuredModel(Protocol):
    def parse[Output: BaseModel](self, messages: list[Message], schema: type[Output]) -> tuple[Output, Usage]: ...


class GEvalJudge:
    def __init__(self, model: StructuredModel) -> None:
        self.model = model

    def evaluate(self, question: str, fragments: list[SearchHit], answer: str, cited: list[Citation]) -> Verdict:
        scores, _ = self.model.parse(judge_messages(question, fragments, answer, cited), GEvalScores)
        return Verdict(
            groundedness=scores.groundedness,
            relevance=scores.relevance,
            citation_correct=(scores.citation_correct - 1) / 4,
            reasoning=scores.reasoning,
            judge="g-eval",
        )


def judge_messages(
    question: str, fragments: list[SearchHit], answer: str, cited: list[Citation]
) -> list[Message]:
    blocks = [
        f"[{number}] {hit.chunk.source}\n{hit.chunk.content}"
        for number, hit in enumerate(fragments, start=1)
    ]
    sources = ", ".join(citation.source for citation in cited) or "ninguna"
    material = "\n\n".join([
        f"Pregunta del cliente:\n{question}",
        "Fragmentos:\n\n" + "\n\n".join(blocks),
        f"Respuesta del asistente:\n{answer}",
        f"Fuentes citadas: {sources}",
    ])
    return [{"role": "system", "content": GEVAL_PROMPT}, {"role": "user", "content": material}]
