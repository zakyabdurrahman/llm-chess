import pytest

from llm_chess_competition.agents import FakeChessAgent
from llm_chess_competition.models import AgentMove, AgentResponseError, parse_agent_response


@pytest.mark.parametrize(
    "response",
    [
        '{"move":"e2e4","explanation":"Controls the centre."}',
        '```json\n{"move":"e2e4","explanation":"Controls the centre."}\n```',
    ],
)
def test_parse_valid_agent_response(response: str) -> None:
    assert parse_agent_response(response) == AgentMove("e2e4", "Controls the centre.")


@pytest.mark.parametrize(
    "response",
    [
        "",
        "not JSON",
        '{"move":"e2e4"}',
        '{"move":"e2e4","explanation":"x","extra":true}',
    ],
)
def test_reject_malformed_agent_response(response: str) -> None:
    with pytest.raises(AgentResponseError):
        parse_agent_response(response)


def test_fake_agent_is_deterministic_and_legal() -> None:
    moves = ["e2e4", "d2d4", "g1f3"]
    first = FakeChessAgent(seed=7).propose_move("white", "fen", moves, [])
    second = FakeChessAgent(seed=7).propose_move("white", "fen", moves, [])
    assert first == second
    assert first.move in moves
