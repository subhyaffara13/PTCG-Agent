
def log_strategy(
    packet: dict[str, Any],
    matched_key: str,
    match_reason: str,
    result: dict[str, Any],
    profile_keys: list[str],
) -> None:
    entry: dict[str, Any] = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
        "agent":     "StrategyAgent",
        "input":     packet,
        "reasoning": {
            "profiles_available": profile_keys,
            "matched_profile":    matched_key,
            "match_reason":       match_reason,
        },
        "output": result,
    }
    _log_buffer.append(entry)


def log_strategy(
    packet: dict[str, Any],
    matched_key: str,
    match_reason: str,
    result: dict[str, Any],
    profile_keys: list[str],
) -> None:
    entry: dict[str, Any] = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
        "agent":     "StrategyAgent",
        "input":     packet,
        "reasoning": {
            "profiles_available": profile_keys,
            "matched_profile":    matched_key,
            "match_reason":       match_reason,
        },
        "output": result,
    }
    _log_buffer.append(entry)


def log_strategy(
    packet: dict[str, Any],
    matched_key: str,
    match_reason: str,
    result: dict[str, Any],
    profile_keys: list[str],
) -> None:
    entry: dict[str, Any] = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
        "agent":     "StrategyAgent",
        "input":     packet,
        "reasoning": {
            "profiles_available": profile_keys,
            "matched_profile":    matched_key,
            "match_reason":       match_reason,
        },
        "output": result,
    }
    _log_buffer.append(entry)

