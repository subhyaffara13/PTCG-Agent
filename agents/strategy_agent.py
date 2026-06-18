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
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", perspective_flag: str = "player", shared_context=None):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.shared_context = shared_context
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"
        self._reasoning_buffer = []  # In-memory buffer, NO disk I/O per turn
        
        self.learned_donts = {"behavior_donts": []}
        donts_path = self.skills_dir / "learned_donts.json"
        if donts_path.exists():
            try:
                self.learned_donts = json.loads(donts_path.read_text(encoding="utf-8"))
            except:
                pass
        
        if self.shared_context:
            self.profiles = self.shared_context.get_config(str(self.skills_dir), "strategy_profiles.json")
        else:
            self.profiles = self._load_strategy_profiles()
            
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

        prized_probabilities = board_summary.get("prized_probabilities", {})
        pikachu_prized_prob = prized_probabilities.get("721", 0.0)
        raichu_prized_prob = prized_probabilities.get("722", 0.0)

        # Trigger logic conditions
        is_prize_gap = (my_prizes - opponent_prizes) >= 2
        is_deck_identified = opponent_confidence > 0.75
        is_hand_shift = (self.last_priority_profile is not None) and (priority_profile != self.last_priority_profile)
        is_explicit = trigger == "force_evaluate" or trigger == "prize_gap"
        is_turn_milestone = turn_number in (3, 6, 9, 12, 15)
        my_bench_count = board_summary.get('my_bench_count', 0)
        is_bench_advantage = my_bench_count >= 3 and opponent_prizes > 3
        is_prized_attacker = (pikachu_prized_prob >= 0.75 or raichu_prized_prob >= 0.75)

        should_trigger = is_prize_gap or is_deck_identified or is_hand_shift or is_explicit or is_turn_milestone or is_bench_advantage or is_prized_attacker

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
        # Apply learned behavior donts to avoid certain strategies
        proposed_strategy = self.active_strategy
        if (pikachu_prized_prob >= 0.75 or raichu_prized_prob >= 0.75) and opponent_prizes > 2:
            proposed_strategy = 'setup'
        elif opponent_prizes <= 2:
            proposed_strategy = 'closing'
        elif my_prizes >= 5 and opponent_prizes <= 3:
            proposed_strategy = 'aggro_push'  # desperation: far behind, must attack
        elif opponent_archetype == 'aggro' and my_prizes < opponent_prizes:
            new_strategy = 'stall'  # only stall when ahead in prizes
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
                logger.error(f"Failed to flush strategy reasoning logs: {e}")
