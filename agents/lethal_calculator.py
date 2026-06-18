"""
agents/lethal_calculator.py

Calculates if lethal damage is on the board.
If my_active_damage >= opponent_active_hp, it overrides the TurnPlanner
and forces the attack to guarantee the win or prize advantage.
"""

import json
import logging
from pathlib import Path
from typing import Any
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class LethalCalculator(BaseAgent):
    def __init__(self, log_dir: str = "logs", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"
        self._reasoning_buffer = []  # In-memory buffer, NO disk I/O per turn
        self._reasoning_buffer = []  # In-memory buffer, NO disk I/O per turn

    def receive(self, packet: Any) -> Any:
        """
        Receives a LethalPacket. 
        Calculates if lethal is possible. Returns an action_override if true.
        """
        my_damage = getattr(packet, "my_active_damage", 0)
        opp_hp = getattr(packet, "opponent_active_hp", 100)
        legal_attacks = getattr(packet, "legal_attacks", [])

        # If we have an attack available and we can KO the opponent's active
        if legal_attacks and my_damage >= opp_hp and my_damage > 0:
            attack_name = legal_attacks[0]
            action = f"attack:{attack_name}"
            reasoning = f"LethalCalculator found lethal: my_damage {my_damage} >= opponent_hp {opp_hp}. Forcing attack."
            
            response = {
                "action_override": action,
                "reasoning_chain": reasoning
            }
            self._log_reasoning(response)
            return response
            
        return {
            "action_override": None,
            "reasoning_chain": "No lethal found."
        }

    def _log_reasoning(self, response: dict):
        log_entry = {
            "agent": "LethalCalculator",
            "action_override": response.get("action_override"),
            "reasoning_chain": response.get("reasoning_chain")
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
                logger.error(f"Failed to flush lethal calculator reasoning logs: {e}")
