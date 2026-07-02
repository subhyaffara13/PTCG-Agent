"""File I/O helpers for StrategyAgent — skill loading and strategy logging."""

from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

from agents.log_flusher import flush_reasoning_logs
import logging

logger = logging.getLogger(__name__)

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH   = _PROJECT_ROOT / "skills" / "strategy_profiles.json"
_LOG_PATH     = _PROJECT_ROOT / "logs"   / "reasoning_log.json"
_log_buffer: list[dict[str, Any]] = []


def flush_logs() -> None:
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
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


def board_signal_match(board_summary: dict[str, Any]) -> str | None:
    prizes     = board_summary.get("prizes")
    bench      = board_summary.get("bench_count")
    score      = board_summary.get("hand_score")
    energy     = board_summary.get("energy_attached")
    opp_prizes = board_summary.get("opponent_prizes")
    boss_prob  = board_summary.get("boss_prob", 0.0)
    iono_prob  = board_summary.get("iono_prob", 0.0)

    if boss_prob > 0.7 and bench is not None and int(bench) > 0: return "stall"
    if iono_prob > 0.7 and score is not None and float(score) > 5.0: return "aggro_push"
    if prizes is not None and int(prizes) <= 2: return "endgame_close"
    if opp_prizes is not None and int(opp_prizes) <= 2: return "prize_race"
    if bench is not None and int(bench) <= 1: return "bench_low"
    if energy is not None and int(energy) == 0: return "energy_stall"
    if score is not None and float(score) < 2.0: return "hand_dead"
        
    p_val = int(prizes) if prizes is not None else 6
    if p_val >= 5: return "setup"
    if p_val >= 3: return "aggro"
    return "endgame_close"


def keyword_scan(trigger_lower: str, profiles: dict[str, Any]) -> tuple[str | None, float]:
    best_key, best_score = None, 0.0
    for key, profile in profiles.items():
        trigger_desc = profile.get("trigger", "").lower()
        words = [w.strip("(),<>=") for w in trigger_desc.split() if len(w) > 3]
        if not words: continue
        matched = sum(1 for w in words if w in trigger_lower)
        score   = matched / len(words)
        if score > best_score:
            best_score, best_key = score, key
    return best_key, best_score
