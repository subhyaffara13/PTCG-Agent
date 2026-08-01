
def _parse_state(observation: Mapping[str, Any]) -> dict[str, Any]:
    """Parse the proxy's JSON observation, returning ``{}`` on any failure."""
    raw = observation.get("observationString", "")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def _parse_state(observation: Mapping[str, Any]) -> dict[str, Any]:
    """Parse the proxy JSON observation, returning ``{}`` on failure."""
    raw = observation.get("observationString", "")
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}

