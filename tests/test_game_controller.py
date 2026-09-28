from collections import deque

from llm_chess_competition.agents import FakeChessAgent
from llm_chess_competition.application import GameController
from llm_chess_competition.domain import ChessGame
from llm_chess_competition.models import AgentMove


class FakeUI:
    def __init__(self, choices: list[str]) -> None:
        self.choices = deque(choices)
        self.messages: list[str] = []

    def write(self, message: str) -> None:
        self.messages.append(message)

    def choose(self) -> str:
        return self.choices.popleft()


class ScriptedAgent:
    def __init__(self, moves: list[str]) -> None:
        self.moves = deque(moves)
        self.calls = 0

    def propose_move(
        self,
        color: str,
        fen: str,
        legal_moves: list[str],
        move_history: list[str],
    ) -> AgentMove:
        self.calls += 1
        return AgentMove(self.moves.popleft(), "test move")


def test_board_does_not_change_before_approval_and_user_can_stop() -> None:
    game = ChessGame()
    before = game.get_fen()
    result = GameController(
        ScriptedAgent(["e2e4"]), FakeChessAgent(), FakeUI(["S"]), game=game
    ).run()
    assert result.status == "stopped"
    assert game.get_fen() == before


def test_board_changes_after_approval_and_turn_alternates() -> None:
    game = ChessGame()
    result = GameController(
        ScriptedAgent(["e2e4"]),
        ScriptedAgent(["e7e5"]),
        FakeUI(["C", "S"]),
        game=game,
    ).run()
    assert result.status == "stopped"
    assert game.get_move_history() == ["e2e4"]
    assert game.turn == "black"


def test_retry_occurs_after_invalid_response() -> None:
    white = ScriptedAgent(["bad", "e2e4"])
    game = ChessGame()
    GameController(white, FakeChessAgent(), FakeUI(["S"]), game=game).run()
    assert white.calls == 2
    assert game.get_move_history() == []


def test_rejection_requests_another_move_without_applying_first() -> None:
    white = ScriptedAgent(["e2e4", "d2d4"])
    game = ChessGame()
    GameController(white, FakeChessAgent(), FakeUI(["R", "S"]), game=game).run()
    assert white.calls == 2
    assert game.get_move_history() == []


def test_three_invalid_responses_produce_technical_forfeit() -> None:
    result = GameController(
        ScriptedAgent(["bad"] * 3), FakeChessAgent(), FakeUI([])
    ).run()
    assert result.status == "forfeit"
    assert result.winner == "black"


def test_checkmate_ends_the_loop() -> None:
    game = ChessGame()
    result = GameController(
        ScriptedAgent(["f2f3", "g2g4"]),
        ScriptedAgent(["e7e5", "d8h4"]),
        FakeUI(["C"] * 4),
        game=game,
    ).run()
    assert result.status == "completed"
    assert result.reason == "checkmate"
    assert result.winner == "black"


def test_fake_agents_can_complete_a_match() -> None:
    class AutoApproveUI:
        def write(self, message: str) -> None:
            pass

        def choose(self) -> str:
            return "C"

    result = GameController(
        FakeChessAgent(seed=1), FakeChessAgent(seed=2), AutoApproveUI()
    ).run()
    assert result.status == "completed"
