"""
cb_agents/turn_planner_logging.py

Helper utilities for TurnPlanner: legal candidate generation and reasoning log management.
"""

import json
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)


def build_legal_candidates(game_state: dict) -> List[str]:
    """Build a list of legal action strings from game_state fields."""
    candidates = []

    for k, prefix in [
        ("legal_attacks", "attack"),
        ("legal_evolutions", "evolve"),
        ("legal_attachments", "attach_energy"),
        ("legal_trainers", "play_trainer"),
        ("legal_bench", "bench"),
        ("legal_retreats", "retreat"),
        ("legal_abilities", "ability"),
    ]:
        for val in game_state.get(k, []):
            candidates.append(f"{prefix}:{val}")

    candidates.append("pass")
    return candidates


class TurnPlannerLogger:
    """Buffers per-turn reasoning entries and flushes them to disk."""

    def __init__(self, log_dir: Path):
        self.reasoning_log_file = log_dir / "reasoning_log.json"
        self._reasoning_buffer: list = []

    def log_reasoning(self, turn: int, profile: str, response: dict):
        """Append a reasoning snapshot to the in-memory buffer."""
        self._reasoning_buffer.append({
            "turn": turn,
            "priority_profile": profile,
            "action_sequence": response["action_sequence"],
            "primary_action": response["primary_action"],
            "reasoning_chain": response["reasoning_chain"],
        })

    def flush_logs(self):
        """Write all buffered logs to disk. Called once at end of game."""
        if self._reasoning_buffer:
            try:
                self.reasoning_log_file.write_text(
                    json.dumps(self._reasoning_buffer, indent=2),
                    encoding="utf-8",
                )
            except Exception as e:
                logger.error(f"Failed to flush turn planner logs: {e}")
            self._reasoning_buffer.clear()
