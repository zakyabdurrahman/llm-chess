from dataclasses import dataclass

from ..agents import ChessAgent
from ..domain import ChessGame
from ..models import AgentMove
from ..ui import GameUI


@dataclass(frozen=True)
class MatchResult:
    status: str
    reason: str
    winner: str | None = None


class GameController:
    def __init__(
        self,
        white_agent: ChessAgent,
        black_agent: ChessAgent,
        ui: GameUI,
        *,
        game: ChessGame | None = None,
        max_retries: int = 3,
    ) -> None:
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1")
        self.game = game or ChessGame()
        self._agents = {"white": white_agent, "black": black_agent}
        self._ui = ui
        self._max_retries = max_retries

    def run(self) -> MatchResult:
        self._show_board()
        while not self.game.is_game_over():
            color = self.game.turn
            proposal = self._get_valid_proposal(color)
            if proposal is None:
                winner = "black" if color == "white" else "white"
                return self._finish(
                    MatchResult(
                        "forfeit",
                        f"{color} failed to provide a valid move",
                        winner,
                    )
                )

            self._ui.write(
                f"{color.title()} proposes {proposal.move}: {proposal.explanation}"
            )
            choice = self._ui.choose()
            if choice == "S":
                return self._finish(MatchResult("stopped", "stopped by user"))
            if choice == "R":
                continue

            self.game.apply_move(proposal.move)
            self._show_board()

        outcome = self.game.get_outcome()
        assert outcome is not None
        return self._finish(
            MatchResult("completed", outcome.termination, outcome.winner),
            outcome.result,
        )

    def _get_valid_proposal(self, color: str) -> AgentMove | None:
        legal_moves = self.game.get_legal_moves()
        for attempt in range(1, self._max_retries + 1):
            try:
                proposal = self._agents[color].propose_move(
                    color,
                    self.game.get_fen(),
                    legal_moves,
                    self.game.get_move_history(),
                )
                if self.game.is_legal_move(proposal.move):
                    return proposal
                error = f"illegal move {proposal.move!r}"
            except Exception as exc:
                error = str(exc) or type(exc).__name__
            self._ui.write(
                f"Invalid {color} response ({attempt}/{self._max_retries}): {error}"
            )
        return None

    def _show_board(self) -> None:
        history = " ".join(self.game.get_move_history()) or "(none)"
        self._ui.write(f"\n{self.game.get_ascii_board()}\nMoves: {history}")

    def _finish(self, result: MatchResult, score: str | None = None) -> MatchResult:
        score_text = f" Result: {score}." if score else ""
        winner_text = f" Winner: {result.winner}." if result.winner else ""
        self._ui.write(f"Match ended: {result.reason}.{score_text}{winner_text}")
        return result
