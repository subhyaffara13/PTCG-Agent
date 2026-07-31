from . import Any, _LOG_PATH, _SKILL_PATH, _log_buffer, datetime, flush_reasoning_logs, json, logger, pathlib

def flush_logs() -> None:
    try:
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    flush_reasoning_logs(_log_buffer, _LOG_PATH, logger)

def load_skill(skills_dir=None) -> dict[str, dict[str, Any]]:
    path = pathlib.Path(skills_dir) / "strategy_profiles.json" if skills_dir else _SKILL_PATH
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raw = {"profiles": {}}
    return raw.get("profiles", {})

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

def _opponent_archetype_signal(board_summary: dict[str, Any]) -> str | None:
    """Adjust strategy based on opponent's identified archetype."""
    arch = board_summary.get("opponent_archetype", "unknown")
    conf = board_summary.get("opponent_archetype_confidence", 0.0)
    if conf < 0.5 or arch == "unknown":
        return None
    raw_prizes = board_summary.get("prizes")
    if raw_prizes is None:
        raw_prizes = board_summary.get("my_prizes_remaining")
    prizes = int(raw_prizes) if raw_prizes is not None else 6
    if arch == "aggro" and prizes <= 4:
        return "disruption"  # Opponent is aggressive — disrupt hand and energy while building counter-push
    if arch == "stall" and prizes >= 4:
        return "aggro"  # Opponent stalls — pressure before they set up
    if arch == "combo" and prizes <= 4:
        return "aggro_push"  # Opponent is building combo — rush before it comes online
    if arch == "control":
        return "setup"  # Opponent controls — outvalue with more resources
    return None

