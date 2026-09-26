import argparse
import getpass
import shelve
from pathlib import Path

import chess
import chess.svg
import cairosvg
from PIL import Image


CACHE_PATH = Path(__file__).resolve().parents[2] / "cache"
CACHE_PATH.mkdir(parents=True, exist_ok=True)
KEY_NAME = "openrouter_key"


def load_key():
    with shelve.open(str(CACHE_PATH)) as cache:
        return cache.get(KEY_NAME)


def save_key(key):
    with shelve.open(str(CACHE_PATH)) as cache:
        cache[KEY_NAME] = key


def reset_key():
    with shelve.open(str(CACHE_PATH)) as cache:
        cache.pop(KEY_NAME, None)


def mask_key(key):
    if len(key) <= 8:
        return "*" * len(key)
    return f"{key[:4]}...{key[-4:]}"


def get_openrouter_key():
    existing = load_key()

    if existing:
        print(f"Found stored OpenRouter key: {mask_key(existing)}")
        use_existing = input("Use existing key? (y/n): ").strip().lower()
        if use_existing in ("y", "yes"):
            return existing

    key = getpass.getpass("Enter Openrouter Key: ").strip()
    if key:
        save_key(key)
    return key


def main():
    parser = argparse.ArgumentParser(description="OpenRouter key cache")
    parser.add_argument(
        "--reset", action="store_true", help="clear the cached OpenRouter key"
    )
    args = parser.parse_args()

    if args.reset:
        reset_key()
        print("Cached OpenRouter key cleared.")
        return

    key = get_openrouter_key()
    print("OpenRouter key loaded." if key else "No key provided.")

    # now here is the call to the game engines (both LLM and chess)
    # this is just testing chess board rendering (produce SVG string)
    board = chess.Board()
    board_svg = chess.svg.board(board)
    png_board = cairosvg.svg2png(bytestring=board_svg.encode('utf-8'))
    # Save temporarily to render as text pixels
    with open(CACHE_PATH / "temp.png", "wb") as f:
      f.write(png_board) # type: ignore

    

    img = Image.open(CACHE_PATH / "temp.png")
    img.show()