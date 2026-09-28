import json
import re
from dataclasses import dataclass


class AgentResponseError(ValueError):
    pass


@dataclass(frozen=True)
class AgentMove:
    move: str
    explanation: str


def parse_agent_response(response: str) -> AgentMove:
    text = response.strip()
    fenced = re.fullmatch(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        text = fenced.group(1)
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError) as exc:
        raise AgentResponseError("Agent response is not valid JSON") from exc
    if not isinstance(data, dict) or set(data) != {"move", "explanation"}:
        raise AgentResponseError("Response must contain only move and explanation")
    if not all(isinstance(data[key], str) and data[key].strip() for key in data):
        raise AgentResponseError("Move and explanation must be non-empty strings")
    return AgentMove(data["move"].strip().lower(), data["explanation"].strip())
