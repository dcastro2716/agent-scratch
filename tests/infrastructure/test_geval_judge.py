from agent.domain.knowledge import Chunk, SearchHit
from agent.domain.models import Usage
from agent.infrastructure.evaluation.geval_judge import GEvalJudge, GEvalScores


class RecordingStructuredModel:
    def __init__(self) -> None:
        self.messages = []

    def parse(self, messages, schema):
        self.messages = messages
        return schema(
            reasoning="Todo está en el fragmento 1.",
            groundedness=5,
            relevance=4,
            citation_correct=3,
        ), Usage()


def test_geval_sends_the_material_and_converts_the_citation_score():
    hit = SearchHit(
        chunk=Chunk(id="c1", content="Plazos: 60 días.", doc_type="faq", section="FAQ", source="faq.md"),
        score=1.0,
    )
    model = RecordingStructuredModel()
    verdict = GEvalJudge(model).evaluate("¿Plazo?", [hit], "60 días.", [])

    assert (verdict.groundedness, verdict.relevance, verdict.citation_correct) == (5, 4, 0.5)
    assert verdict.reasoning == "Todo está en el fragmento 1."
    assert verdict.judge == "g-eval"
    material = model.messages[1]["content"]
    assert "[1] faq.md\nPlazos: 60 días." in material
    assert "Pregunta del cliente:\n¿Plazo?" in material
    assert "Respuesta del asistente:\n60 días." in material
    assert "Fuentes citadas: ninguna" in material
    assert list(GEvalScores.model_fields)[0] == "reasoning"
