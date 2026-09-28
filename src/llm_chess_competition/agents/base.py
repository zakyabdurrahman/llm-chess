from typing import Protocol

from ..models import AgentMove


class ChessAgent(Protocol):
    def propose_move(
        self,
        color: str,
        fen: str,
        legal_moves: list[str],
        move_history: list[str],
    ) -> AgentMove: ...
