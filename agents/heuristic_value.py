"""
agents/heuristic_value.py

Provides the heuristic value network logic used by MCTS.
"""

import random
import logging
from agents.value_network import BaseValueNetwork

logger = logging.getLogger(__name__)

class HeuristicValueNetwork(BaseValueNetwork):
    """
    Hand-tuned heuristic value network extracted from the original MCTSEngine._evaluate_state.
    """

    def evaluate(self, game_state: dict, action: str = None, determinization: dict = None) -> float:
        if action is None:
            return 0.0

        value = 0.0

        # 1. State Heuristics (Prize Velocity, Active HP delta, attached resources)
        my_prizes = game_state.get("my_prizes", 6)
        opp_prizes = game_state.get("opponent_prizes", 6)
        prize_delta = opp_prizes - my_prizes
        value += 0.15 * prize_delta

        my_active_hp = game_state.get("my_active_hp", 100)
        opp_active_hp = game_state.get("opponent_active_hp", 100)
        hp_delta = my_active_hp - opp_active_hp
        value += 0.001 * hp_delta

        # Evolution Progress
        my_bench = game_state.get("my_bench", [])
        my_active = game_state.get("my_active_pokemon", {})
        all_my_pokemon = my_bench + ([my_active] if isinstance(my_active, dict) and my_active else [])
        evo_count = 0
        for p in all_my_pokemon:
            if isinstance(p, dict):
                card_id = p.get("id")
                if card_id:
                    try:
                        from agents.card_registry import CardRegistry
                        card_entry = CardRegistry().get(card_id)
                        if card_entry and card_entry.stage in ("Stage 1", "Stage 2"):
                            evo_count += 1
                    except:
                        pass
        value += 0.05 * evo_count

        # 2. Threat Penalty from belief determinization
        threat_penalty = 0.0
        if determinization and determinization.get("hand"):
            threat_penalty = len(determinization["hand"]) * 0.01

        # 3. Action-based adjustments
        if action.startswith("attack:"):
            value += 0.5
            if my_prizes <= 1:
                value += 0.5
        elif action.startswith("evolve:"):
            value += 0.3
        elif action.startswith("attach_energy:"):
            value += 0.2
            active_pokemon = game_state.get("my_active_pokemon")
            if isinstance(active_pokemon, dict):
                card_id = active_pokemon.get("id")
                attached_count = len(active_pokemon.get("attached", []))
                try:
                    from agents.card_registry import CardRegistry
                    registry = CardRegistry()
                    card_entry = registry.get_full_skill(card_id)
                    needed = card_entry.energy_cost if card_entry else 3
                except Exception:
                    needed = 3 if card_id == 722 else 2
                if attached_count >= needed:
                    value -= 0.7  # Penalize over-attaching energy!
        elif action.startswith("bench:"):
            value += 0.8 if not my_bench else 0.15
        elif action.startswith("play_trainer:"):
            value += 0.4
            my_deck_count = game_state.get("my_deck_count", 60)
            if my_deck_count <= 5:
                trainer_name = action.split(":", 1)[1].lower()
                draw_keywords = ["research", "iono", "judge", "draw"]
                if any(k in trainer_name for k in draw_keywords):
                    value -= 1.3
        elif action.startswith("retreat:"):
            if my_active_hp <= 60:
                value += 0.4
            else:
                value -= 0.2
        elif action == "pass":
            value -= 0.5

        value -= threat_penalty
        value += random.uniform(-0.01, 0.01)
        return max(-1.0, min(1.0, value))
