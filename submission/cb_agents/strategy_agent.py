"""
agents/strategy_agent.py

Evaluates macro game states on key trigger events, selects high-level strategy profiles,
and reports dynamic directive states. Kept under 100 lines.
"""

import json
import logging
from pathlib import Path
from typing import Any
from cb_agents.base_agent import BaseAgent
from router.bus import StrategyPacket
from cb_agents.registry import register_agent
from cb_agents.strategy_helpers import check_should_trigger, select_new_strategy
from cb_agents.log_flusher import flush_reasoning_logs

logger = logging.getLogger(__name__)


@register_agent("strategy_agent")
class StrategyAgent(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills",
                 perspective_flag: str = "player", shared_context=None):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.shared_context = shared_context
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"
        self._reasoning_buffer = []
        
        self.profiles = self._load_json("strategy_profiles.json", {"profiles": {}})
        self.strategy_thresholds = self._load_json("strategy_thresholds.json", {})

        self.active_strategy = "aggro_push"
        self.last_triggered_turn = -1
        self.last_priority_profile = None

    def _load_json(self, name: str, default: dict) -> dict:
        ctx = self.shared_context
        if not ctx:
            try:
                from cb_agents.context import SharedContext
                ctx = SharedContext()
            except Exception: pass
        if ctx:
            return ctx.get_config(str(self.skills_dir), name) or default
        path = self.skills_dir / name
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to load {name}: {e}")
        return default

    def receive(self, packet: Any) -> dict:
        if not isinstance(packet, StrategyPacket):
            raise TypeError(f"StrategyAgent received an illegal packet type: {type(packet).__name__}.")

        board = packet.board_summary or {}
        priority_profile = board.get("priority_profile", "aggro_push")
        turn = board.get("turn_number", 1)

        should_trigger, sa_config = check_should_trigger(
            board, packet.trigger, self.last_priority_profile, self.strategy_thresholds
        )
        self.last_priority_profile = priority_profile

        if not should_trigger:
            self._log_reasoning(turn, packet.trigger, self.active_strategy, self.active_strategy, False, "No trigger condition met")
            return {"new_strategy": self.active_strategy, "reasoning": "No trigger condition met", "triggered": False, "turn_triggered": turn}

        prev_strategy = self.active_strategy
        self.active_strategy = select_new_strategy(board, self.active_strategy, sa_config)
        self.last_triggered_turn = turn

        reasoning = f"Evaluated new strategy {self.active_strategy} via trigger context check."
        self._log_reasoning(turn, packet.trigger, prev_strategy, self.active_strategy, True, reasoning)

        return {"new_strategy": self.active_strategy, "reasoning": reasoning, "triggered": True, "turn_triggered": turn}

    def _log_reasoning(self, turn: int, trigger_reason: str, prev_strat: str, 
                      new_strat: str, triggered: bool, reasoning: str):
        self._reasoning_buffer.append({
            "turn_triggered": turn,
            "trigger_reason": trigger_reason,
            "previous_strategy": prev_strat,
            "new_strategy": new_strat,
            "triggered": triggered,
            "reasoning": reasoning
        })

    def flush_logs(self):
        """Write all buffered logs to disk. Called once at end of game."""
        flush_reasoning_logs(self._reasoning_buffer, self.reasoning_log_file, logger)
