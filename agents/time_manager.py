"""
agents/time_manager.py

Monitors elapsed game time and forces speed thresholds or pass actions
as limits are approached to prevent timeout forfeits.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict
from agents.base_agent import BaseAgent
from router.bus import TimePacket

logger = logging.getLogger(__name__)

class TimeManager(BaseAgent):
    def __init__(self, log_dir: str = "logs", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.time_limit = 600.0
        self.warning_threshold = 540.0
        self.force_pass_threshold = 570.0
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"
        self._reasoning_buffer = []  # In-memory buffer, NO disk I/O per turn
        self._reasoning_buffer = []  # In-memory buffer, NO disk I/O per turn

    def receive(self, packet: Any) -> dict:
        """
        Accepts and processes TimePacket. Returns timeout overrides.
        """
        # Type check validation
        if not isinstance(packet, TimePacket):
            raise TypeError(
                f"TimeManager received an illegal packet type: {type(packet).__name__}."
            )

        time_elapsed = getattr(packet, "time_elapsed", 0.0)
        
        # Negative or missing check
        if time_elapsed is None or time_elapsed < 0.0:
            time_elapsed = 0.0
            self._log_warning("Negative or missing time_elapsed in TimePacket. Treated as 0.0.")

        # Hardcoded limit enforcement
        limit = self.time_limit
        time_remaining = max(0.0, limit - time_elapsed)

        # Timeout state logical checks
        if time_elapsed < 540.0:
            status = "normal"
            action_override = None
            urgent = False
        elif 540.0 <= time_elapsed < 570.0:
            status = "warning"
            action_override = "fastest_legal_move"
            urgent = True
        elif 570.0 <= time_elapsed < 600.0:
            status = "critical"
            action_override = "pass"
            urgent = True
        else: # >= 600
            status = "timeout"
            action_override = "forfeit"
            urgent = True

        return {
            "status": status,
            "action_override": action_override,
            "time_remaining": round(time_remaining, 2),
            "urgent": urgent
        }

    def _log_warning(self, msg: str):
        logger.warning(msg)
        log_entry = {
            "turn": "n/a",
            "hand_score": 0.0,
            "priority_profile": "n/a",
            "top_play": "n/a",
            "reasoning_chain": f"TIME MANAGER WARNING: {msg}"
        }
        self._reasoning_buffer.append(log_entry)

    def flush_logs(self):
        """Write all buffered logs to disk. Called once at end of game."""
        if self._reasoning_buffer:
            try:
                logs = []
                if self.reasoning_log_file.exists():
                    content = self.reasoning_log_file.read_text(encoding="utf-8").strip()
                    if content:
                        try:
                            logs = json.loads(content)
                            if not isinstance(logs, list):
                                logs = [logs]
                        except json.JSONDecodeError:
                            logs = []
                logs.extend(self._reasoning_buffer)
                self.reasoning_log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
                self._reasoning_buffer.clear()
            except Exception as e:
                logger.error(f"Failed to flush time manager warning logs: {e}")
