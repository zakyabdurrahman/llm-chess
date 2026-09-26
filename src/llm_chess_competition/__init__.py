import argparse
import getpass
import shelve
from pathlib import Path
from .engine.ChessAgentFactory import ChessAgentFactory

import os


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

    os.environ['OPENROUTER_API_KEY'] = key

    agent_factory = ChessAgentFactory()

    maid_agent = agent_factory.make_agent("xiaomi/mimo-v2.6-pro")

    result = maid_agent.invoke({"messages": [{"role": "user", "content": "Hello"}]})

    print(result['messages'])
    
    