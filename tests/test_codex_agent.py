from dataclasses import dataclass

import pytest

from llm_chess_competition.agents.codex_agent import CodexChessAgent
from llm_chess_competition.models import AgentMove, AgentResponseError


@dataclass
class Result:
    final_response: str | None
    error: object | None = None


class Turn:
    def __init__(self, result: Result) -> None:
        self.result = result

    def run(self) -> Result:
        return self.result


class Thread:
    def __init__(self, result: Result) -> None:
        self.result = result
        self.prompt = ""
        self.schema: dict[str, object] = {}

    def turn(self, prompt: str, *, output_schema: dict[str, object]) -> Turn:
        self.prompt = prompt
        self.schema = output_schema
        return Turn(self.result)


def test_codex_agent_parses_structured_response() -> None:
    thread = Thread(Result('{"move":"e2e4","explanation":"Controls the centre."}'))
    move = CodexChessAgent(thread).propose_move(
        "white", "test-fen", ["e2e4"], []
    )
    assert move == AgentMove("e2e4", "Controls the centre.")
    assert "test-fen" in thread.prompt
    assert thread.schema["additionalProperties"] is False


def test_codex_agent_rejects_empty_or_malformed_response() -> None:
    with pytest.raises(RuntimeError, match="empty"):
        CodexChessAgent(Thread(Result(None))).propose_move("white", "fen", ["e2e4"], [])
    with pytest.raises(AgentResponseError):
        CodexChessAgent(Thread(Result("not JSON"))).propose_move("white", "fen", ["e2e4"], [])
