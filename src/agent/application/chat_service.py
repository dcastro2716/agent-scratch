import json
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass

from agent.domain.errors import AgentError, ErrorKind
from agent.domain.knowledge import Citation, SearchHit
from agent.domain.models import (
    AgentReply,
    AgentTurn,
    AnswerDelta,
    Intent,
    IntentDetected,
    Message,
    ModelEvent,
    ModelResult,
    ToolCall,
    ToolRequest,
    ToolResult,
    ToolStatus,
    TurnEvent,
    Usage,
)
from agent.domain.ports import ChatModel, ConversationStore, Embedder, KnowledgeBase, QueryRewriter, Tools

MAX_TOOL_ROUNDS = 5  # criterio de terminación: sin esto, un modelo confundido pide tools para siempre

REWRITE_PROMPT = (
    "Reescribe la última pregunta del cliente para que se entienda sola, sin leer la conversación. "
    "Conserva los productos, montos y fechas que se mencionaron antes. No la respondas."
)
CONTEXT_HEADER = (
    "Fragmentos del corpus para la última pregunta. Si es product_question, responde solo con ellos y pon en "
    "el campo sources los números que usaste; si no tienen la respuesta, dilo. No escribas los números dentro de la respuesta."
)
TOOLS_HEADER = (
    "Tienes tools del banco para consultar los datos del cliente y para pedir acciones. Para datos del cliente usa las "
    "tools: nunca inventes montos, fechas ni estados. Si ninguna tool sirve para lo que piden, dilo. Una acción sensible "
    "se propone con su tool cuando el cliente la pide explícitamente o confirma que quiere proceder. Si tienes los "
    "argumentos requeridos, llama a la tool en ese turno; no pidas otra confirmación. Si falta un argumento, pide "
    "solo ese dato. La aprobación de un asesor es posterior a la llamada y se requiere antes de registrar o "
    "ejecutar la acción. Resuelve referencias como esa o esa comisión con el historial: si acabas de ofrecer "
    "la devolución de una comisión, usa su código en la tool. La confirmación del cliente autoriza proponer "
    "la acción a revisión. No requiere una segunda confirmación del cliente."
)
PENDING_APPROVAL_MESSAGE = (
    "La acción queda pendiente de aprobación de un asesor. Aún no se ha registrado ni ejecutado."
)
PENDING_APPROVAL = json.dumps(
    {"status": "pendiente_aprobacion", "detail": PENDING_APPROVAL_MESSAGE},
    ensure_ascii=False,
)
UNCONFIRMED_ACTION_MESSAGE = (
    "No se ha registrado ni ejecutado ninguna acción. Indícame qué acción quieres solicitar y los datos necesarios."
)


@dataclass(frozen=True)
class PreparedTurn:
    """Lo que se arma antes de llamar al modelo: la pregunta, los mensajes con el contexto y lo que se encontró."""

    user: Message
    messages: list[Message]
    hits: list[SearchHit]
    rewrite_usage: Usage


class ChatService:
    """Caso de uso: resolver un turno de conversación con RAG y tools. Solo conoce puertos, nunca infraestructura."""

    def __init__(
        self,
        model: ChatModel,
        rewriter: QueryRewriter,
        embedder: Embedder,
        knowledge_base: KnowledgeBase,
        store: ConversationStore,
        system_prompt: str,
        max_turns: int,
        top_k: int,
        tools: Tools | None = None,  # sin tools (MCP_URL vacío), el agente responde solo con RAG
    ) -> None:
        self.model = model
        self.rewriter = rewriter
        self.embedder = embedder
        self.knowledge_base = knowledge_base
        self.store = store
        self.system_prompt = system_prompt
        self.max_turns = max_turns
        self.top_k = top_k
        self.tools = tools
        self.tool_definitions = tools.definitions() if tools else []

    def handle(self, session_id: str, message: str) -> AgentTurn:
        prepared = self._prepare(session_id, message)
        *_, turn = self._answer(session_id, prepared, lambda messages: [self.model.complete(messages, self.tool_definitions)])
        return turn

    def handle_stream(self, session_id: str, message: str) -> Iterator[TurnEvent]:
        """Igual que handle, pero entrega la respuesta mientras el modelo la escribe.

        Reescribir y buscar ocurren aquí mismo, antes de devolver los eventos: si fallan, el AgentError sale de inmediato
        y la API todavía puede responder con su código HTTP (502, 504, 429).
        """
        prepared = self._prepare(session_id, message)
        return self._answer(session_id, prepared, lambda messages: self.model.stream(messages, self.tool_definitions))

    def _prepare(self, session_id: str, message: str) -> PreparedTurn:
        user: Message = {"role": "user", "content": message}
        recent = self.store.get(session_id)[-self.max_turns * 2 :]

        query, rewrite_usage = message, Usage()
        if recent:  # la primera pregunta ya se entiende sola: no se gasta una llamada en reescribirla
            rewritten = self.rewriter.rewrite([{"role": "system", "content": REWRITE_PROMPT}, *recent, user])
            query, rewrite_usage = rewritten.query, rewritten.usage
        hits = self.knowledge_base.search(query, self.embedder.embed([query])[0], self.top_k)

        context: Message = {"role": "system", "content": _context_message(hits)}
        system: list[Message] = [{"role": "system", "content": self.system_prompt}]
        if self.tool_definitions:
            system.append({"role": "system", "content": TOOLS_HEADER})
        messages = [*system, *recent, context, user]
        return PreparedTurn(user=user, messages=messages, hits=hits, rewrite_usage=rewrite_usage)

    def _answer(
        self, session_id: str, prepared: PreparedTurn, ask: Callable[[list[Message]], Iterable[ModelEvent]]
    ) -> Iterator[TurnEvent]:
        """El ciclo ReAct: el modelo pide tools, el agente las ejecuta y le devuelve lo que pasó, hasta que responde."""
        messages, usage, used = list(prepared.messages), prepared.rewrite_usage, []
        for _ in range(MAX_TOOL_ROUNDS):
            sensitive_reply = False
            for event in ask(messages):
                match event:
                    case ModelResult():
                        if event.reply.intent == Intent.SENSITIVE_ACTION and self.tool_definitions:
                            yield from self._sensitive_reply(
                                session_id, prepared, UNCONFIRMED_ACTION_MESSAGE, usage + event.usage, used
                            )
                            return
                        yield self._finish(session_id, prepared, event.reply, usage + event.usage, used)
                        return
                    case ToolRequest(calls=calls):
                        usage += event.usage
                    case IntentDetected(intent=Intent.SENSITIVE_ACTION) if self.tool_definitions:
                        sensitive_reply = True
                    case AnswerDelta() if sensitive_reply:
                        continue
                    case _:
                        yield event
            messages.append(_assistant_asking(calls))
            for call in calls:
                yield call
                result = self._run(call)
                used.append(result)
                yield result
                messages.append({"role": "tool", "tool_call_id": call.id, "content": result.content})
            if any(result.status == ToolStatus.PENDING_APPROVAL for result in used):
                yield from self._sensitive_reply(session_id, prepared, PENDING_APPROVAL_MESSAGE, usage, used)
                return
        raise AgentError(ErrorKind.INVALID_OUTPUT, f"el modelo pidió tools {MAX_TOOL_ROUNDS} veces seguidas sin responder")

    def _sensitive_reply(
        self, session_id: str, prepared: PreparedTurn, answer: str, usage: Usage, tools: list[ToolResult]
    ) -> Iterator[TurnEvent]:
        reply = AgentReply(intent=Intent.SENSITIVE_ACTION, answer=answer, sources=[])
        yield IntentDetected(intent=reply.intent)
        yield AnswerDelta(text=reply.answer)
        yield self._finish(session_id, prepared, reply, usage, tools)

    def _run(self, call: ToolCall) -> ToolResult:
        definition = next((tool for tool in self.tool_definitions if tool.name == call.name), None)
        if definition is None or self.tools is None:
            return ToolResult(call=call, status=ToolStatus.ERROR, content=f"La tool {call.name} no existe.")
        if definition.sensitive:  # S8: aquí entra la aprobación humana
            return ToolResult(call=call, status=ToolStatus.PENDING_APPROVAL, content=PENDING_APPROVAL)
        return self.tools.call(call)

    def _finish(
        self, session_id: str, prepared: PreparedTurn, reply: AgentReply, usage: Usage, tools: list[ToolResult]
    ) -> AgentTurn:
        # se guarda solo si el turno terminó: un error, aunque sea a mitad del streaming, no deja turnos
        # a medias. El contexto no se guarda: cada turno busca de nuevo, y el historial no crece con fragmentos viejos
        self.store.append(session_id, prepared.user)
        self.store.append(session_id, {"role": "assistant", "content": reply.answer})
        return AgentTurn(
            reply=reply,
            usage=usage,
            citations=_citations_from(reply.sources, prepared.hits),
            tools=tools,
            hits=prepared.hits,
        )


def _assistant_asking(calls: list[ToolCall]) -> Message:
    """El pedido del modelo, en los mensajes del turno: para entender cada resultado, el modelo necesita ver qué pidió."""
    return {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {"id": call.id, "type": "function",
             "function": {"name": call.name, "arguments": json.dumps(call.arguments, ensure_ascii=False)}}
            for call in calls
        ],
    }


def _context_message(hits: list[SearchHit]) -> str:
    if not hits:
        return "No se encontraron fragmentos del corpus para esta pregunta."
    blocks = [f"[{number}] {hit.chunk.source}\n{hit.chunk.content}" for number, hit in enumerate(hits, start=1)]
    return "\n\n".join([CONTEXT_HEADER, *blocks])


def _citations_from(numbers: list[int], hits: list[SearchHit]) -> list[Citation]:
    # el modelo solo elige números; uno que no existe se descarta, así ninguna cita es inventada
    cited_chunks = [hits[number - 1].chunk for number in dict.fromkeys(numbers) if 1 <= number <= len(hits)]
    return [Citation(source=chunk.source, section=chunk.section, chunk_id=chunk.id) for chunk in cited_chunks]
