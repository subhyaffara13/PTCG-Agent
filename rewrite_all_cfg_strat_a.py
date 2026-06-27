# First part of agents/strategy_agent.py content

STRATEGY_AGENT_A = """\
\"\"\"
agents/strategy_agent.py
------------------------
Selects the optimal board strategy given a trigger event and board summary.

Contract
--------
- Skill file  : skills/strategy_profiles.json  (loaded once at __init__, never again)
- Input packet: { trigger: str, board_summary: dict }  -- from Router only
- Output      : { strategy: str, posture: str, actions: list[str],
                  escalation: str, confidence: float }
- Logs        : every evaluation -> logs/reasoning_log.json
- File access : strategy_profiles.json and reasoning_log.json ONLY

Matching priority
-----------------
1. Exact key match against profiles dict
2. Board-summary signal heuristics
3. Keyword scan of profile trigger descriptions
4. Fallback to 'hand_dead' profile
\"\"\"

from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

_PROJECT_ROOT         = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH           = _PROJECT_ROOT / "skills" / "strategy_profiles.json"
_LOG_PATH             = _PROJECT_ROOT / "logs"   / "reasoning_log.json"
_CONF_EXACT_KEY       = 1.0
_CONF_KEYWORD         = 0.75
_CONF_FALLBACK        = 0.3
_FALLBACK_PROFILE_KEY = "hand_dead"


class StrategyAgent:
    def __init__(self) -> None:
        self._profiles: dict[str, dict[str, Any]] = self._load_skill()

    def evaluate(self, packet: dict[str, Any]) -> dict[str, Any]:
        trigger: str        = str(packet.get("trigger", "")).strip()
        board_summary: dict = packet.get("board_summary", {})
        profile_key, profile, confidence, match_reason = self._match_profile(trigger, board_summary)
        result: dict[str, Any] = {
            "strategy":   profile_key,
            "posture":    profile.get("posture", "tempo"),
            "actions":    profile.get("actions", ["PASS"]),
            "escalation": profile.get("escalation", "PASS"),
            "confidence": round(confidence, 4),
        }
        self._log(packet, profile_key, match_reason, result)
        return result

    def _load_skill(self) -> dict[str, dict[str, Any]]:
        raw = json.loads(_SKILL_PATH.read_text(encoding="utf-8"))
        return raw.get("profiles", {})

    def _match_profile(self, trigger, board_summary):
        trigger_lower = trigger.lower()
        if trigger_lower in self._profiles:
            return trigger_lower, self._profiles[trigger_lower], _CONF_EXACT_KEY, "exact key match"
        board_match = self._board_signal_match(board_summary)
        if board_match:
            return board_match, self._profiles[board_match], _CONF_KEYWORD, f"board_summary signal -> {board_match}"
        best_key, best_score = self._keyword_scan(trigger_lower)
        if best_key and best_score > 0:
            return (best_key, self._profiles[best_key],
                    _CONF_KEYWORD * best_score, f"keyword scan score={best_score:.2f}")
        fallback = self._profiles.get(_FALLBACK_PROFILE_KEY, {})
        return _FALLBACK_PROFILE_KEY, fallback, _CONF_FALLBACK, "no match -> fallback"
"""
