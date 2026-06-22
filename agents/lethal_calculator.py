"""
agents/lethal_calculator.py

Calculates if lethal damage is on the board.
If my_active_damage >= opponent_active_hp, it overrides the TurnPlanner
and forces the attack to guarantee the win or prize advantage.
"""

import logging
from pathlib import Path
from typing import Any
from agents.base_agent import BaseAgent
from agents.log_flusher import flush_reasoning_logs
from agents.registry import register_agent

logger = logging.getLogger(__name__)

@register_agent("lethal_calculator", needs_skills_dir=False, needs_shared_context=False)
class LethalCalculator(BaseAgent):
    def __init__(self, log_dir: str = "logs", perspective_flag: str = "player"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.reasoning_log_file = self.log_dir / "reasoning_log.json"
        self._reasoning_buffer = []  # In-memory buffer, NO disk I/O per turn

    def receive(self, packet: Any) -> Any:
        """
        Receives a LethalPacket. 
        Calculates if lethal is possible. Returns an action_override if true.
        """
        my_damage = getattr(packet, "my_active_damage", 0)
        opp_hp = getattr(packet, "opponent_active_hp", 100)
        legal_attacks = getattr(packet, "legal_attacks", [])

        # 1. Check if we have an attack available and we can KO the opponent's active (our lethal)
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

        # 2. Check if opponent can KO us next turn (opponent's lethal threat)
        opp_active_id = getattr(packet, "opponent_active_id", None)
        my_hp = getattr(packet, "my_active_hp", 100)
        legal_retreats = getattr(packet, "legal_retreats", [])

        if opp_active_id is not None:
            try:
                from agents.card_registry import CardRegistry
                registry = CardRegistry()
                opp_card = registry.get_full_skill(opp_active_id)
                if opp_card and opp_card.damage_output >= my_hp and opp_card.damage_output > 0:
                    if legal_retreats:
                        retreat_target = legal_retreats[0]
                        action = f"retreat:{retreat_target}"
                        reasoning = f"LethalCalculator found opponent lethal threat: opp_damage {opp_card.damage_output} >= my_hp {my_hp}. Forcing retreat to {retreat_target}."
                        response = {
                            "action_override": action,
                            "reasoning_chain": reasoning
                        }
                        self._log_reasoning(response)
                        return response
            except Exception as e:
                logger.error(f"Error checking opponent lethal threat in registry: {e}")
            
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
        flush_reasoning_logs(self._reasoning_buffer, self.reasoning_log_file, logger)
