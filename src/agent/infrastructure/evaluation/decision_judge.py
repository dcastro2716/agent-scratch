import json
import urllib.error
import urllib.request
from typing import Any

from agent.domain.errors import AgentError, ErrorKind
from agent.domain.evaluation import Verdict
from agent.domain.knowledge import Citation, SearchHit
from agent.infrastructure.llm.credentials import Credential

GROUNDEDNESS_LEVELS = [
    "Inventada: no está en los fragmentos o los contradice",
    "Mayormente inventada",
    "La mitad está en los fragmentos",
    "Casi todo está en los fragmentos",
    "Todo está en los fragmentos",
]
RELEVANCE_LEVELS = [
    "No contesta la pregunta",
    "Contesta muy poco",
    "Contesta una parte",
    "Contesta casi todo",
    "Contesta exactamente lo que se preguntó",
]


class DecisionJudge:
    """Evalúa respuestas con el modelo Decision-1 de Microsoft Foundry."""

    def __init__(self, endpoint: str, credential: Credential, deployment: str, timeout_s: float) -> None:
        self.url = f"{endpoint.rstrip('/')}/providers/microsoft/v1/systemone"
        self.credential = credential
        self.deployment = deployment
        self.timeout_s = timeout_s

    def evaluate(self, question: str, fragments: list[SearchHit], answer: str, cited: list[Citation]) -> Verdict:
        body = decision_request(self.deployment, question, fragments, answer, cited)
        request = urllib.request.Request(
            self.url,
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json", **_authorization(self.credential)},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                return verdict_from(json.loads(response.read()))
        except urllib.error.HTTPError as error:
            raise AgentError(ErrorKind.UPSTREAM, f"decision-1 respondió {error.code}") from error
        except TimeoutError as error:
            raise AgentError(ErrorKind.TIMEOUT, "decision-1 no respondió a tiempo") from error
        except urllib.error.URLError as error:
            if isinstance(error.reason, TimeoutError):
                raise AgentError(ErrorKind.TIMEOUT, "decision-1 no respondió a tiempo") from error
            raise AgentError(ErrorKind.UPSTREAM, "no se pudo conectar con decision-1") from error
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise AgentError(ErrorKind.INVALID_OUTPUT, "decision-1 no devolvió JSON válido") from error


def _authorization(credential: Credential) -> dict[str, str]:
    if callable(credential):
        return {"Authorization": f"Bearer {credential()}"}
    return {"api-key": credential}


def decision_request(
    deployment: str, question: str, fragments: list[SearchHit], answer: str, cited: list[Citation]
) -> dict[str, Any]:
    """Agrupa los tres criterios de evaluación en una sola solicitud."""
    return {
        "model": deployment,
        "state": {
            "question": question,
            "fragments": [
                {"number": number, "source": hit.chunk.source, "text": hit.chunk.content}
                for number, hit in enumerate(fragments, start=1)
            ],
            "answer": answer,
            "cited_sources": [citation.source for citation in cited],
        },
        "questions": {
            "groundedness": {
                "type": "score",
                "instructions": "¿Todo lo que afirma la respuesta está en los fragmentos?",
                "criteria": GROUNDEDNESS_LEVELS,
            },
            "relevance": {
                "type": "score",
                "instructions": "¿La respuesta contesta lo que preguntó el cliente?",
                "criteria": RELEVANCE_LEVELS,
            },
            "citation_correct": {
                "type": "noul",
                "instructions": "¿Las fuentes citadas contienen lo que afirma la respuesta?",
                "criteria": {
                    "true": "Las fuentes citadas respaldan la respuesta",
                    "false": "Las fuentes citadas no la respaldan, o no se citó ninguna",
                },
            },
        },
    }


def verdict_from(payload: object) -> Verdict:
    answers = payload.get("answers") if isinstance(payload, dict) else None
    if not isinstance(answers, dict):
        raise AgentError(ErrorKind.INVALID_OUTPUT, "decision-1 no devolvió las calificaciones")
    return Verdict(
        groundedness=_number(answers, "groundedness", "score", 4) + 1,
        relevance=_number(answers, "relevance", "score", 4) + 1,
        citation_correct=_number(answers, "citation_correct", "noul", 1),
        judge="decision-1",
    )


def _number(answers: dict[str, Any], question: str, field: str, maximum: int) -> float:
    answer = answers.get(question)
    value = answer.get(field) if isinstance(answer, dict) else None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= maximum:
        raise AgentError(ErrorKind.INVALID_OUTPUT, f"decision-1 no devolvió un número válido para {question}")
    return float(value)
