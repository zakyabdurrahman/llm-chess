import argparse
import getpass
import shelve
from pathlib import Path
from .engine.GameLoop import GameLoop

import os


CACHE_DIR = Path(__file__).resolve().parents[2] / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
KEY_DB = CACHE_DIR / "key"
KEY_NAME = "openrouter_key"


def clear_cache_pngs():
    for png in CACHE_DIR.glob("*.png"):
        png.unlink()


def load_key():
    with shelve.open(str(KEY_DB)) as cache:
        return cache.get(KEY_NAME)


def save_key(key):
    with shelve.open(str(KEY_DB)) as cache:
        cache[KEY_NAME] = key


def reset_key():
    with shelve.open(str(KEY_DB)) as cache:
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
    clear_cache_pngs()

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

    os.environ['OPENROUTER_API_KEY'] = key

    game_loop = GameLoop()
    game_loop.initAgents()
    
    