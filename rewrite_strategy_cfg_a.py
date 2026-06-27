"""First part of strategy_agent.py content."""

STRATEGY_AGENT_CONTENT_A = """\
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
- Logs reasoning to logs/reasoning_log.json
- No other file access permitted

Matching logic
--------------
1. Exact key match against profiles dict (e.g. "prize_race")
2. Board-summary signal heuristics
3. Keyword scan of profile trigger descriptions
4. Fallback to "hand_dead" profile
\"\"\"

from __future__ import annotations

import json
import pathlib
import datetime
from typing import Any

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH   = _PROJECT_ROOT / "skills" / "strategy_profiles.json"
_LOG_PATH     = _PROJECT_ROOT / "logs"   / "reasoning_log.json"

_CONF_EXACT_KEY       = 1.0
_CONF_KEYWORD         = 0.75
_CONF_FALLBACK        = 0.3
_FALLBACK_PROFILE_KEY = "hand_dead"


class StrategyAgent:
    \"\"\"Selects the best strategic posture for the current board state.

    Usage
    -----
        agent  = StrategyAgent()
        result = agent.evaluate(packet)
        # {strategy, posture, actions, escalation, confidence}
    \"\"\"

    def __init__(self) -> None:
        self._profiles: dict[str, dict[str, Any]] = self._load_skill()

    # -- public API -----------------------------------------------------------

    def evaluate(self, packet: dict[str, Any]) -> dict[str, Any]:
        trigger: str        = str(packet.get("trigger", "")).strip()
        board_summary: dict = packet.get("board_summary", {})

        profile_key, profile, confidence, match_reason = self._match_profile(
            trigger, board_summary
        )

        result: dict[str, Any] = {
            "strategy":   profile_key,
            "posture":    profile.get("posture", "tempo"),
            "actions":    profile.get("actions", ["PASS"]),
            "escalation": profile.get("escalation", "PASS"),
            "confidence": round(confidence, 4),
        }

        self._log(packet, profile_key, match_reason, result)
        return result

    # -- internals ------------------------------------------------------------

    def _load_skill(self) -> dict[str, dict[str, Any]]:
        raw = json.loads(_SKILL_PATH.read_text(encoding="utf-8"))
        return raw.get("profiles", {})
"""
