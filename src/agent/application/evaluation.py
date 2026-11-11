import re
import unicodedata
from collections.abc import Iterable, Sequence
from statistics import mean
from uuid import uuid4

from agent.application.chat_service import ChatService
from agent.application.redaction import contains_personal_data
from agent.domain.evaluation import CaseResult, EvalSummary, GoldenCase
from agent.domain.models import Intent
from agent.domain.ports import Judge


class EvaluateAgent:
    """Ejecuta cada caso del golden set con el mismo servicio del chat."""

    def __init__(self, chat_service: ChatService, judge: Judge) -> None:
        self.chat_service = chat_service
        self.judge = judge

    def run_case(self, case: GoldenCase) -> CaseResult:
        session_id = f"eval-{case.id}-{uuid4().hex}"
        for previous_message in case.history:
            self.chat_service.handle(session_id, previous_message)
        turn = self.chat_service.handle(session_id, case.question)

        answer = turn.reply.answer
        cited = [citation.source for citation in turn.citations]
        retrieved = [hit.chunk.source for hit in turn.hits]
        expected_sources = set(case.expected_sources)
        forbidden_cited = bool(set(cited) & set(case.forbidden_sources))
        if expected_sources:
            sources_ok = bool(set(cited) & expected_sources) and not forbidden_cited
        else:
            sources_ok = not cited
        judged = case.expected_intent is Intent.PRODUCT_QUESTION and bool(turn.hits)

        return CaseResult(
            case_id=case.id,
            case_type=case.type,
            answer=answer,
            intent=turn.reply.intent,
            cited_sources=cited,
            retrieved_sources=retrieved,
            recall=bool(set(retrieved) & expected_sources) if expected_sources else None,
            intent_ok=turn.reply.intent is case.expected_intent,
            sources_ok=sources_ok,
            facts_ok=facts_found(answer, case.key_facts) if case.key_facts else None,
            personal_data_leak=contains_personal_data(answer),
            forbidden_cited=forbidden_cited,
            verdict=self.judge.evaluate(case.question, turn.hits, answer, turn.citations) if judged else None,
            usage=turn.usage,
        )


def facts_found(answer: str, key_facts: list[str]) -> bool:
    """Comprueba los hechos clave ignorando mayúsculas, tildes y espacios extra."""
    normalized_answer = _normalize(answer)
    return all(_normalize(fact) in normalized_answer for fact in key_facts)


def _normalize(text: str) -> str:
    without_accents = unicodedata.normalize("NFKD", text.lower()).encode("ascii", "ignore").decode()
    return " ".join(re.sub(r"[^\w%/.,$-]+", " ", without_accents).split())


def summarize(results: Sequence[CaseResult]) -> EvalSummary:
    verdicts = [result.verdict for result in results if result.verdict is not None]
    return EvalSummary(
        cases=len(results),
        recall_at_k=_share(result.recall for result in results),
        intent_accuracy=_share(result.intent_ok for result in results),
        sources_ok=_share(result.sources_ok for result in results),
        facts_ok=_share(result.facts_ok for result in results),
        groundedness=mean(verdict.groundedness for verdict in verdicts) if verdicts else None,
        relevance=mean(verdict.relevance for verdict in verdicts) if verdicts else None,
        citation_correct=mean(verdict.citation_correct for verdict in verdicts) if verdicts else None,
        personal_data_leaks=sum(result.personal_data_leak for result in results),
        forbidden_citations=sum(result.forbidden_cited for result in results),
        prompt_tokens=sum(result.usage.prompt_tokens for result in results),
        completion_tokens=sum(result.usage.completion_tokens for result in results),
    )


def _share(checks: Iterable[bool | None]) -> float:
    applicable = [check for check in checks if check is not None]
    return mean(applicable) if applicable else 0.0
