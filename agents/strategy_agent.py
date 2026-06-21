"""
agents/strategy_agent.py

Evaluates macro game states on key trigger events, selects high-level strategy profiles,
and reports dynamic directive states.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict
from agents.base_agent import BaseAgent
from router.bus import StrategyPacket
from agents.registry import register_agent
from agents.strategy_helpers import check_should_trigger, select_new_strategy

logger = logging.getLogger(__name__)

@register_agent("strategy_agent")
class StrategyAgent(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player", shared_context=None):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.shared_context = shared_context
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"
        self._reasoning_buffer = []
        
        self.profiles = {"profiles": {}}
        if self.shared_context:
            try:
                self.profiles = self.shared_context.get_config(str(self.skills_dir), "strategy_profiles.json")
                if not isinstance(self.profiles, dict):
                    self.profiles = {"profiles": {}}
            except Exception:
                pass
        else:
            self.profiles = self._load_strategy_profiles()
            
        self.strategy_thresholds = {}
        if self.shared_context:
            try:
                self.strategy_thresholds = self.shared_context.get_config(str(self.skills_dir), "strategy_thresholds.json")
            except Exception as e:
                logger.error(f"Failed to load strategy_thresholds.json: {e}")
        else:
            try:
                from agents.context import SharedContext
                self.strategy_thresholds = SharedContext().get_config(str(self.skills_dir), "strategy_thresholds.json")
            except Exception:
                thresh_path = self.skills_dir / "strategy_thresholds.json"
                if thresh_path.exists():
                    try:
                        self.strategy_thresholds = json.loads(thresh_path.read_text(encoding="utf-8"))
                    except Exception as e:
                        logger.error(f"Failed to load strategy_thresholds.json directly: {e}")

        self.active_strategy = "aggro_push"
        self.last_triggered_turn = -1
        self.last_priority_profile = None

    def _load_strategy_profiles(self) -> dict:
        path = self.skills_dir / "strategy_profiles.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read strategy_profiles.json: {e}")
        return {"profiles": {}}

    def receive(self, packet: Any) -> dict:
        if not isinstance(packet, StrategyPacket):
            raise TypeError(f"StrategyAgent received an illegal packet type: {type(packet).__name__}.")

        board_summary = packet.board_summary or {}
        priority_profile = board_summary.get("priority_profile", "aggro_push")
        turn_number = board_summary.get("turn_number", 1)

        # EVALUATE SHOULD TRIGGER
        should_trigger, sa_config = check_should_trigger(
            board_summary, packet.trigger, self.last_priority_profile, self.strategy_thresholds
        )

        self.last_priority_profile = priority_profile

        if not should_trigger:
            response = {
                "new_strategy": self.active_strategy,
                "reasoning": "No trigger condition met",
                "triggered": False,
                "turn_triggered": turn_number
            }
            self._log_reasoning(turn_number, packet.trigger, self.active_strategy, self.active_strategy, False, "No trigger condition met")
            return response

        # CHOOSE NEW STRATEGY
        prev_strategy = self.active_strategy
        new_strategy = select_new_strategy(board_summary, self.active_strategy, sa_config)

        self.active_strategy = new_strategy
        self.last_triggered_turn = turn_number

        reasoning = f"Evaluated new strategy {new_strategy} via trigger context check."
        
        response = {
            "new_strategy": new_strategy,
            "reasoning": reasoning,
            "triggered": True,
            "turn_triggered": turn_number
        }

        self._log_reasoning(turn_number, packet.trigger, prev_strategy, new_strategy, True, reasoning)
        return response

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
                logger.error(f"Failed to flush strategy reasoning logs: {e}")
