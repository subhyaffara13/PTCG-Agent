"""Helper: rewrite strategy_agent.py with the correct content."""
import pathlib

content = """\
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

    def _match_profile(
        self,
        trigger: str,
        board_summary: dict[str, Any],
    ) -> tuple[str, dict[str, Any], float, str]:
        trigger_lower = trigger.lower()

        # Pass 1: exact key
        if trigger_lower in self._profiles:
            return trigger_lower, self._profiles[trigger_lower], _CONF_EXACT_KEY, "exact key match"

        # Pass 2: board_summary signals
        board_match = self._board_signal_match(board_summary)
        if board_match:
            key = board_match
            return key, self._profiles[key], _CONF_KEYWORD, f"board_summary signal -> {key}"

        # Pass 3: keyword scan
        best_key, best_score = self._keyword_scan(trigger_lower)
        if best_key and best_score > 0:
            return (
                best_key,
                self._profiles[best_key],
                _CONF_KEYWORD * best_score,
                f"keyword scan score={best_score:.2f}",
            )

        # Pass 4: fallback
        fallback = self._profiles.get(_FALLBACK_PROFILE_KEY, {})
        return _FALLBACK_PROFILE_KEY, fallback, _CONF_FALLBACK, "no match -> fallback"

    def _board_signal_match(self, board_summary: dict[str, Any]) -> str | None:
        prizes     = board_summary.get("prizes")
        bench      = board_summary.get("bench_count")
        score      = board_summary.get("hand_score")
        energy     = board_summary.get("energy_attached")
        opp_prizes = board_summary.get("opponent_prizes")

        if prizes is not None and int(prizes) <= 2:
            return "endgame_close"
        if opp_prizes is not None and int(opp_prizes) <= 2:
            return "prize_race"
        if bench is not None and int(bench) <= 1:
            return "bench_low"
        if energy is not None and int(energy) == 0:
            return "energy_stall"
        if score is not None and float(score) < 2.0:
            return "hand_dead"
        return None

    def _keyword_scan(self, trigger_lower: str) -> tuple[str | None, float]:
        best_key, best_score = None, 0.0
        for key, profile in self._profiles.items():
            trigger_desc = profile.get("trigger", "").lower()
            words = [w.strip("(),<>=") for w in trigger_desc.split() if len(w) > 3]
            if not words:
                continue
            matched = sum(1 for w in words if w in trigger_lower)
            score   = matched / len(words)
            if score > best_score:
                best_score, best_key = score, key
        return best_key, best_score

    def _log(
        self,
        packet: dict[str, Any],
        matched_key: str,
        match_reason: str,
        result: dict[str, Any],
    ) -> None:
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":     "StrategyAgent",
            "input":     packet,
            "reasoning": {
                "profiles_available": list(self._profiles.keys()),
                "matched_profile":    matched_key,
                "match_reason":       match_reason,
            },
            "output": result,
        }
        try:
            log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
"""

target = pathlib.Path("agents/strategy_agent.py")
target.write_text(content, encoding="utf-8")
print(f"Written {target}  ({target.stat().st_size} bytes)")
