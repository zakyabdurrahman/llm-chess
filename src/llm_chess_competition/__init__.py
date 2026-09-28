import argparse

from .agents.codex_agent import CodexAgentProvider
from .agents.fake_agent import FakeChessAgent
from .application import GameController
from .ui import TerminalUI


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Watch two agents play chess")
    parser.add_argument("--provider", choices=("codex", "fake"), default="fake")
    parser.add_argument("--white-model")
    parser.add_argument("--black-model")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--max-retries", type=int, default=3)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    ui = TerminalUI()
    try:
        if args.provider == "fake":
            GameController(
                FakeChessAgent(args.seed),
                FakeChessAgent(args.seed + 1),
                ui,
                max_retries=args.max_retries,
            ).run()
        else:
            with CodexAgentProvider(args.white_model, args.black_model) as agents:
                GameController(*agents, ui, max_retries=args.max_retries).run()
    except KeyboardInterrupt:
        ui.write("\nMatch stopped.")
    except Exception as exc:
        ui.write(f"Error: {exc}")


__all__ = ["main"]
