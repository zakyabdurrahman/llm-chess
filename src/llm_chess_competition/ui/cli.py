from typing import Protocol


class GameUI(Protocol):
    def write(self, message: str) -> None: ...

    def choose(self) -> str: ...


class TerminalUI:
    def write(self, message: str) -> None:
        print(message)

    def choose(self) -> str:
        while True:
            choice = input("[C]ontinue, [R]eject, or [S]top: ").strip().upper()
            if choice in {"C", "R", "S"}:
                return choice
            self.write("Please enter C, R, or S.")
