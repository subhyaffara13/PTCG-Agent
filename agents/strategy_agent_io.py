"""File I/O helpers for StrategyAgent — skill loading and strategy logging."""

import json
import pathlib
import datetime
from typing import Any

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH   = _PROJECT_ROOT / "skills" / "strategy_profiles.json"
_LOG_PATH     = _PROJECT_ROOT / "logs"   / "reasoning_log.json"
_log_buffer: list[dict[str, Any]] = []


def flush_logs() -> None:
    if not _log_buffer:
        return
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        log = []
    log.extend(_log_buffer)
    _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
    _log_buffer.clear()


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
        "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
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
