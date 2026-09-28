import chess
import pytest

from llm_chess_competition.domain import ChessGame


def test_standard_starting_position() -> None:
    game = ChessGame()
    assert game.get_fen() == chess.STARTING_FEN
    assert len(game.get_legal_moves()) == 20
    assert game.turn == "white"


def test_legal_move_is_accepted() -> None:
    game = ChessGame()
    assert game.is_legal_move("e2e4")
    game.apply_move("e2e4")
    assert game.get_move_history() == ["e2e4"]
    assert game.turn == "black"


def test_illegal_move_is_rejected_without_changing_board() -> None:
    game = ChessGame()
    before = game.get_fen()
    assert not game.is_legal_move("e2e5")
    with pytest.raises(ValueError, match="Illegal move"):
        game.apply_move("e2e5")
    assert game.get_fen() == before
