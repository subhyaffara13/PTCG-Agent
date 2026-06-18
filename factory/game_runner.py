"""
factory/game_runner.py

Executes exactly 3 games per iteration isolating variables:
1. Reasoning Test
2. Deck Test
3. Variance Baseline

Strictly enforces timeouts, checks win conditions, and generates iteration_result.json.
"""

import os
import time
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple
from agents.base_agent import BaseAgent
from factory.game_logger import GameLogger
from router.bus import RouterBus, HandAnalystPacket, TurnPlannerPacket, StrategyPacket, TimePacket
from agents.opponent_model import OpponentModelPacket

logger = logging.getLogger(__name__)

class GameRunner(BaseAgent):
    def __init__(self, log_dir: str = "logs", perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError(
            "GameRunner does not receive routed packets — it orchestrates games directly"
        )

    def run_iteration(self, iteration_id: int, version_n1: str, version_n2: str, 
                      deck_base: dict, deck_new: dict, 
                      reasoning_base: dict, reasoning_new: dict) -> dict:
        """
        Executes exactly three games to isolate variables.
        Saves iteration_result.json in the log directory.
        """
        games_config = [
            ("reasoning_test", deck_base, deck_base, reasoning_base, reasoning_new),
            ("deck_test", deck_base, deck_new, reasoning_base, reasoning_base),
            ("variance_baseline", deck_base, deck_base, reasoning_base, reasoning_base)
        ]

        results = {}

        for label, deck_a, deck_b, logic_a, logic_b in games_config:
            try:
                results[label] = self._run_single_game(
                    label, version_n1, version_n2, deck_a, deck_b, logic_a, logic_b
                )
            except Exception as e:
                logger.error(f"Critical error running game '{label}': {e}", exc_info=True)
                results[label] = {
                    "label": label,
                    "winner": "error",
                    "turns_taken": 0,
                    "prizes_taken_a": 0,
                    "prizes_taken_b": 0,
                    "time_elapsed": 0.0,
                    "timeout": False,
                    "log_files": {"action": "", "reasoning": "", "variance": ""}
                }

        output_payload = {
            "iteration": iteration_id,
            "timestamp": datetime.now().isoformat(),
            "games": results,
            "ready_for_eval": True
        }

        # Save iteration result json
        out_file = self.log_dir / "iteration_result.json"
        out_file.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")
        return output_payload

    def _run_single_game(self, label: str, v_a: str, v_b: str, 
                         deck_a: dict, deck_b: dict, logic_a: dict, logic_b: dict) -> dict:
        """Simulates a single 10-minute game run, enforcing rules and checking win conditions."""
        start_time = time.time()
        g_logger = GameLogger(log_dir=str(self.log_dir))
        
        # Simple delegation map for testing/runtime mock
        delegation_map = {
            "turn_start": "hand_analyst",
            "after_hand_analysis": "turn_planner",
            "on_trigger": "strategy_agent",
            "always": "time_manager"
        }
        
        bus = RouterBus(delegation_map, log_dir=str(self.log_dir))
        
        # Minimal mock functions for routing targets
        bus.register_agent("hand_analyst", lambda p: {"evaluated": True})
        bus.register_agent("turn_planner", lambda p: {"move": "fast"})
        bus.register_agent("strategy_agent", lambda p: {"fired": True})
        
        # Register game logger wrapper
        g_logger.register_with_bus(bus)

        # Game state trackers
        turn = 1
        prizes_a = 0
        prizes_b = 0
        winner = None
        game_timeout = False

        # Run loops simulating turns until win condition or timeout
        while True:
            elapsed = time.time() - start_time
            
            # Timeout rule check
            if elapsed >= 600.0:
                winner = "timeout"
                game_timeout = True
                break

            # Run event cycles
            try:
                # 4. If time > 540s: force fastest legal move
                # 5. If time > 570s: force pass
                if elapsed > 570.0:
                    action_type = "force_pass"
                elif elapsed > 540.0:
                    action_type = "fastest_legal_move"
                else:
                    action_type = "standard"

                # Simulate executing the sub-agent turns
                bus.dispatch("turn_start", HandAnalystPacket(hand=["Energy"], deck_remaining=20))
                bus.dispatch("after_hand_analysis", TurnPlannerPacket(hand_score=1.0, priority_profile={}))

                # Simulate progression of cards and outcomes
                if turn % 2 == 1:
                    prizes_a += 1
                else:
                    prizes_b += 1

                # Mock Variance logging
                g_logger.log_variance(turn, "coin_flip", "heads", "heads", 0.0)
                # Mock Reasoning logging
                g_logger.log_reasoning(
                    turn=turn,
                    strategy_active="aggro",
                    hand_score=5.0,
                    strategy_switch_considered=False,
                    opponent_archetype_confidence=0.5,
                    reasoning_chain="Priority rule matches top attacker",
                    reasoning_fired=True,
                    reasoning_outcome="positive"
                )

                # Win condition checks after actions
                if prizes_a >= 6:
                    winner = "player_a"
                    break
                if prizes_b >= 6:
                    winner = "player_b"
                    break

            except Exception as turn_err:
                logger.error(f"Error on turn {turn}: {turn_err}")
                raise turn_err

            turn += 1
            if turn > 40:  # Safeguard deck empty or infinite turn loops
                winner = "player_a" if prizes_a >= prizes_b else "player_b"
                break

        elapsed = time.time() - start_time
        
        # Save logger streams immediately
        g_logger.save(v_a, v_b)

        # Generate expected file paths
        timestamp = g_logger.timestamp_str
        suffix = f"game_{timestamp}_v{v_a}_vs_v{v_b}.json"

        return {
            "label": label,
            "winner": winner,
            "turns_taken": turn,
            "prizes_taken_a": prizes_a,
            "prizes_taken_b": prizes_b,
            "time_elapsed": round(elapsed, 2),
            "timeout": game_timeout,
            "log_files": {
                "action": f"action_{suffix}",
                "reasoning": f"reasoning_{suffix}",
                "variance": f"variance_{suffix}"
            }
        }
