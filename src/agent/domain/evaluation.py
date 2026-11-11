"""Evaluación del RAG: casos del golden set, nota del juez y resultado de cada caso."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from agent.domain.models import Intent, Usage


class CaseType(StrEnum):
    ANSWERABLE = "answerable"
    FOLLOW_UP = "follow_up"
    EXPIRED = "expired"
    NOISE = "noise"
    OUT_OF_SCOPE = "out_of_scope"
    PERSONAL_DATA = "personal_data"


class GoldenCase(BaseModel):
    """Un caso del golden set: la pregunta y lo que se espera del agente."""

    model_config = ConfigDict(extra="forbid")

    id: str
    type: CaseType
    history: list[str] = []
    question: str
    expected_intent: Intent
    expected_sources: list[str] = []
    forbidden_sources: list[str] = []
    key_facts: list[str] = []


class Verdict(BaseModel):
    """La nota del juez sobre una respuesta."""

    groundedness: float  # de 1 a 5
    relevance: float  # de 1 a 5
    citation_correct: float  # de 0 a 1
    reasoning: str = ""  # solo G-Eval explica su nota
    judge: str


class CaseResult(BaseModel):
    """Resultado de un caso. None indica que el control no aplica."""

    case_id: str
    case_type: CaseType
    answer: str
    intent: Intent
    cited_sources: list[str]
    retrieved_sources: list[str]
    recall: bool | None
    intent_ok: bool
    sources_ok: bool
    facts_ok: bool | None
    personal_data_leak: bool
    forbidden_cited: bool
    verdict: Verdict | None
    usage: Usage


class EvalSummary(BaseModel):
    """El promedio de cada control sobre los casos donde aplica."""

    cases: int
    recall_at_k: float
    intent_accuracy: float
    sources_ok: float
    facts_ok: float
    groundedness: float | None
    relevance: float | None
    citation_correct: float | None
    personal_data_leaks: int
    forbidden_citations: int
    prompt_tokens: int
    completion_tokens: int
