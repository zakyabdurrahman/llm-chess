import random

from ..models import AgentMove


class FakeChessAgent:
    def __init__(self, seed: int = 0) -> None:
        self._random = random.Random(seed)

    def propose_move(
        self,
        color: str,
        fen: str,
        legal_moves: list[str],
        move_history: list[str],
    ) -> AgentMove:
        if not legal_moves:
            raise ValueError("No legal moves available")
        return AgentMove(
            self._random.choice(legal_moves),
            f"{color.title()} selects a legal move.",
        )
