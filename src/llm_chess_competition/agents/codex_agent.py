import json
from types import TracebackType
from typing import Any

from ..models import AgentMove, parse_agent_response

_MOVE_SCHEMA = {
    "type": "object",
    "properties": {
        "move": {"type": "string"},
        "explanation": {"type": "string"},
    },
    "required": ["move", "explanation"],
    "additionalProperties": False,
}


class CodexChessAgent:
    def __init__(self, thread: Any) -> None:
        self._thread = thread

    def propose_move(
        self,
        color: str,
        fen: str,
        legal_moves: list[str],
        move_history: list[str],
    ) -> AgentMove:
        prompt = (
            "You are playing chess. Select exactly one move from the supplied legal "
            "UCI moves and give a concise explanation. Do not provide private reasoning. "
            "Return only JSON matching the schema.\n"
            f"Color: {color}\nFEN: {fen}\n"
            f"Legal moves: {json.dumps(legal_moves)}\n"
            f"Move history: {json.dumps(move_history)}"
        )
        result = self._thread.turn(prompt, output_schema=_MOVE_SCHEMA).run()
        if result.error:
            raise RuntimeError(str(result.error))
        if not result.final_response:
            raise RuntimeError("Codex returned an empty response")
        return parse_agent_response(result.final_response)


class CodexAgentProvider:
    """Owns one Codex client and two isolated threads for a match."""

    def __init__(
        self,
        white_model: str | None = None,
        black_model: str | None = None,
    ) -> None:
        self._models = (white_model, black_model)
        self._client: Any = None

    def __enter__(self) -> tuple[CodexChessAgent, CodexChessAgent]:
        try:
            from openai_codex import Codex, Sandbox
        except ImportError as exc:
            raise RuntimeError("Codex SDK is not installed; run `uv sync`") from exc

        try:
            self._client = Codex()
            self._client.__enter__()
            if self._client.account().account is None:
                raise RuntimeError("Codex is not authenticated; run `codex login`")
            threads = [
                self._client.thread_start(
                    model=model,
                    sandbox=Sandbox.read_only,
                    ephemeral=True,
                )
                for model in self._models
            ]
            return CodexChessAgent(threads[0]), CodexChessAgent(threads[1])
        except Exception as exc:
            self.__exit__(type(exc), exc, exc.__traceback__)
            if isinstance(exc, RuntimeError):
                raise
            raise RuntimeError(f"Could not start Codex: {exc}") from exc

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._client is not None:
            self._client.__exit__(exc_type, exc, traceback)
