
def _parse_observation(observation: Mapping[str, Any]) -> dict[str, Any] | None:
    """Pull the JSON observation emitted by ``DarkHexState.observation_string``."""
    raw = observation.get("observationString")
    if not raw:
        return None
    try:
        return json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return None


def _parse_observation(text: str) -> dict[str, Any]:
    """Parse the OpenSpiel gin_rummy observation_string into a dict."""
    lines = text.split("\n")
    result: dict[str, Any] = {
        "knock_card": None,
        "prev_upcard": None,
        "repeated_move": 0,
        "phase": None,
        "stock_size": 0,
        "upcard": None,
        "discard_pile": [],
        "hands": {"0": [], "1": []},
        "deadwood": {"0": None, "1": None},
    }
    current_hand: int | None = None
    for line in lines:
        m = _HEADER_RE.match(line)
        if m:
            key = m.group(1).lower().replace(" ", "_")
            value = m.group(2).strip()
            if key == "knock_card":
                result["knock_card"] = int(value) if value.isdigit() else (value or None)
            elif key == "prev_upcard":
                result["prev_upcard"] = _parse_card(value)
            elif key == "repeated_move":
                result["repeated_move"] = int(value)
            elif key == "phase":
                result["phase"] = value
            # current_player from header is redundant with state.current_player()
            continue
        m = _STOCK_RE.match(line)
        if m:
            result["stock_size"] = int(m.group(1))
            result["upcard"] = _parse_card(m.group(2))
            continue
        m = _DISCARD_RE.match(line)
        if m:
            result["discard_pile"] = _CARD_RE.findall(m.group(1))
            continue
        m = _PLAYER_DEADWOOD_RE.match(line)
        if m:
            current_hand = int(m.group(1))
            result["deadwood"][str(current_hand)] = int(m.group(2))
            continue
        m = _PLAYER_RE.match(line)
        if m:
            current_hand = int(m.group(1))
            continue
        if current_hand is not None and line.startswith("|") and line.endswith("|"):
            result["hands"][str(current_hand)].extend(_CARD_RE.findall(line))
    return result


def _parse_observation(observation: Mapping[str, Any]) -> dict[str, Any]:
    """Parse the JSON observation_string emitted by the gin_rummy proxy."""
    raw = observation.get("observationString", "")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return {}


def _parse_observation(observation: Mapping[str, Any]) -> dict[str, Any]:
    obs_str = observation.get("observationString", "")
    if not obs_str:
        return {}
    try:
        return json.loads(obs_str)
    except (json.JSONDecodeError, TypeError):
        return {}


def _parse_observation(observation: Mapping[str, Any]) -> dict[str, Any]:
    """Parse the snake proxy's JSON observation, returning ``{}`` on error."""
    obs_str = observation.get("observationString", "")
    if not obs_str:
        return {}
    try:
        return json.loads(obs_str)
    except (json.JSONDecodeError, TypeError):
        return {}

