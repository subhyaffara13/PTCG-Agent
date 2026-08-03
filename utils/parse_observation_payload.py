import json
from typing import Any

def parse_observation_payload(observation: Mapping[str, Any]) -> dict[str, Any]:
    """Pull the structured bargaining state dict out of the observation.

    Same fallback chain as :mod:`harness`: prefer the proxy's JSON
    ``observationString``; if absent, deserialize the pyspiel state and ask
    it directly.
    """
    raw = observation.get("observationString", "") or ""
    if raw:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
    serialized = observation.get("serializedGameAndState", "")
    if serialized:
        _, state = pyspiel.deserialize_game_and_state(serialized)
        player_id = int(observation.get("playerId", 0))
        try:
            return json.loads(state.observation_string(player_id))
        except (json.JSONDecodeError, RuntimeError):
            pass
    return {}

