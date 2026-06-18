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

logger = logging.getLogger(__name__)

class StrategyAgent(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.profiles = self._load_strategy_profiles()
        self.active_strategy = "aggro_push"
        self.last_triggered_turn = -1
        self.last_priority_profile = None
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"

    def _load_strategy_profiles(self) -> dict:
        path = self.skills_dir / "strategy_profiles.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read strategy_profiles.json: {e}")
        return {"profiles": {}}

    def receive(self, packet: Any) -> dict:
        """
        Accepts and processes StrategyPacket. Evaluates macro priorities when triggered.
        """
        if not isinstance(packet, StrategyPacket):
            raise TypeError(
                f"StrategyAgent received an illegal packet type: {type(packet).__name__}."
            )

        trigger = packet.trigger
        board_summary = packet.board_summary or {}

        # Read board state values safely
        my_prizes = board_summary.get("my_prizes_remaining", 6)
        opponent_prizes = board_summary.get("opponent_prizes_remaining", 6)
        opponent_confidence = board_summary.get("opponent_archetype_confidence", 0.0)
        priority_profile = board_summary.get("priority_profile", "aggro_push")
        turn_number = board_summary.get("turn_number", 1)
        my_active_hp = board_summary.get("my_active_hp", 100)
        opponent_archetype = board_summary.get("opponent_archetype", "unknown")
        bench_has_attacker = board_summary.get("bench_has_attacker", False)

        # Trigger logic conditions
        is_prize_gap = (opponent_prizes - my_prizes) >= 2
        is_deck_identified = opponent_confidence > 0.75
        is_hand_shift = (self.last_priority_profile is not None) and (priority_profile != self.last_priority_profile)
        is_explicit = trigger == "force_evaluate"

        should_trigger = is_prize_gap or is_deck_identified or is_hand_shift or is_explicit

        # Cache last profile state
        self.last_priority_profile = priority_profile

        if not should_trigger:
            response = {
                "new_strategy": self.active_strategy,
                "reasoning": "No trigger condition met",
                "triggered": False,
                "turn_triggered": turn_number
            }
            self._log_reasoning(turn_number, trigger, self.active_strategy, self.active_strategy, False, "No trigger condition met")
            return response

        # Strategy selection logic (in priority order)
        prev_strategy = self.active_strategy
        
        if opponent_archetype == "aggro" and my_prizes > 3:
            new_strategy = "stall"
        elif opponent_prizes <= 2 and my_prizes > opponent_prizes:
            new_strategy = "aggro_push"
        elif my_active_hp < 30 and bench_has_attacker:
            new_strategy = "setup"
        elif opponent_archetype == "control":
            new_strategy = "disruption"
        else:
            new_strategy = self.active_strategy  # no change

        # Update instance state parameters
        self.active_strategy = new_strategy
        self.last_triggered_turn = turn_number

        reasoning = f"Evaluated new strategy {new_strategy} via trigger context check."
        
        response = {
            "new_strategy": new_strategy,
            "reasoning": reasoning,
            "triggered": True,
            "turn_triggered": turn_number
        }

        self._log_reasoning(turn_number, trigger, prev_strategy, new_strategy, True, reasoning)
        return response

    def _log_reasoning(self, turn: int, trigger_reason: str, prev_strat: str, 
                      new_strat: str, triggered: bool, reasoning: str):
        log_entry = {
            "turn_triggered": turn,
            "trigger_reason": trigger_reason,
            "previous_strategy": prev_strat,
            "new_strategy": new_strat,
            "triggered": triggered,
            "reasoning": reasoning
        }
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
            logs.append(log_entry)
            self.reasoning_log_file.write_text(json.dumps(logs, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to log strategy choice: {e}")
