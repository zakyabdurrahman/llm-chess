from dataclasses import dataclass

import chess


@dataclass(frozen=True)
class GameOutcome:
    result: str
    termination: str
    winner: str | None


class ChessGame:
    """Chess rules and state, with python-chess as the sole authority."""

    def __init__(self, fen: str | None = None) -> None:
        self._board = chess.Board(fen) if fen else chess.Board()

    @property
    def turn(self) -> str:
        return "white" if self._board.turn == chess.WHITE else "black"

    def get_fen(self) -> str:
        return self._board.fen()

    def get_ascii_board(self) -> str:
        return str(self._board)

    def get_legal_moves(self) -> list[str]:
        return [move.uci() for move in self._board.legal_moves]

    def is_legal_move(self, move: str) -> bool:
        try:
            return chess.Move.from_uci(move) in self._board.legal_moves
        except (AttributeError, ValueError):
            return False

    def apply_move(self, move: str) -> None:
        if not self.is_legal_move(move):
            raise ValueError(f"Illegal move: {move}")
        self._board.push_uci(move)

    def get_move_history(self) -> list[str]:
        return [move.uci() for move in self._board.move_stack]

    def is_game_over(self) -> bool:
        return self._board.is_game_over(claim_draw=True)

    def get_outcome(self) -> GameOutcome | None:
        outcome = self._board.outcome(claim_draw=True)
        if outcome is None:
            return None
        winner = None if outcome.winner is None else ("white" if outcome.winner else "black")
        return GameOutcome(
            result=outcome.result(),
            termination=outcome.termination.name.replace("_", " ").lower(),
            winner=winner,
        )
