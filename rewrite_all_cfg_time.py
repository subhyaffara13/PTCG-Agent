# Content for agents/time_manager.py

TIME_MANAGER = """\
\"\"\"
agents/time_manager.py
----------------------
Monitors elapsed game time and enforces strict timeout-avoidance policy.

Contract
--------
- No skill file -- operates on hard-wired timing thresholds only.
- Input packet: { time_elapsed: float, time_limit: float } -- from Router only
- Output      : { directive: str, mode: str, urgency: float, time_remaining: float }
- Runs on every tick -- never sleeps, never blocks.
- Guarantees the game never times out.

Timing policy (spec)
--------------------
    time_elapsed <= 540 s  -> NORMAL    -- planner decides freely
    540 < elapsed <= 570 s -> FAST_MOVE -- force fastest legal move immediately
    elapsed > 570 s        -> FORCE_PASS -- force pass to avoid timeout
\"\"\"

from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

_PROJECT_ROOT         = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH             = _PROJECT_ROOT / "logs" / "reasoning_log.json"
_THRESHOLD_FAST       = 540.0
_THRESHOLD_FORCE_PASS = 570.0


class TimeManager:
    def tick(self, packet: dict[str, Any]) -> dict[str, Any]:
        time_elapsed: float = float(packet.get("time_elapsed", 0.0))
        time_limit:   float = float(packet.get("time_limit",  600.0))
        directive, mode     = self._classify(time_elapsed)
        urgency             = self._urgency(time_elapsed, time_limit)
        time_remaining      = max(0.0, time_limit - time_elapsed)
        result: dict[str, Any] = {
            "directive":      directive,
            "mode":           mode,
            "urgency":        round(urgency, 4),
            "time_remaining": round(time_remaining, 2),
        }
        self._log(packet, result)
        return result

    @staticmethod
    def _classify(time_elapsed: float) -> tuple[str, str]:
        if time_elapsed > _THRESHOLD_FORCE_PASS:
            return "FORCE_PASS", "critical"
        if time_elapsed > _THRESHOLD_FAST:
            return "FAST_MOVE", "urgent"
        return "NORMAL", "standard"

    @staticmethod
    def _urgency(time_elapsed: float, time_limit: float) -> float:
        if time_limit <= 0:
            return 1.0
        return min(1.0, max(0.0, time_elapsed / time_limit))

    def _log(self, packet, result):
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":     "TimeManager",
            "input":     packet,
            "reasoning": {
                "threshold_fast":       _THRESHOLD_FAST,
                "threshold_force_pass": _THRESHOLD_FORCE_PASS,
                "evaluation": f"time_elapsed={packet.get('time_elapsed')} -> directive={result['directive']}",
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
