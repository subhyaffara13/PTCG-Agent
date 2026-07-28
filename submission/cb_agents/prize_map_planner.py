"""
cb_agents/prize_map_planner.py

Calculates the optimal 6-prize target path for the agent:
- Identifies opponent 2-prizers vs 1-prizers on board
- Evaluates shortest path to 6 prizes (e.g. 2+2+2 vs 2+2+1+1)
- Assigns priority boosts to Boss's Orders targeting 2-prizers on the optimal path
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger("PrizeMapPlanner")


class PrizeMapPlanner:
    def __init__(self, registry=None):
        self.registry = registry

    def _get_registry(self):
        if not self.registry:
            from cb_agents.card_registry import CardRegistry
            self.registry = CardRegistry()
        return self.registry

    def calculate_prize_path(self, game_state: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates optimal prize target path and returns priority boosts."""
        my_prizes_remaining = game_state.get("my_prizes", 6)
        opp_active = game_state.get("opponent_active_pokemon") or {}
        opp_bench = game_state.get("opponent_bench", [])

        reg = self._get_registry()

        # Collect opponent active & bench targets with prize yields
        targets = []
        if isinstance(opp_active, dict) and opp_active.get("id"):
            cid = opp_active.get("id")
            card = reg.get_full_skill(cid)
            name = getattr(card, "card_name", "") if card else str(opp_active.get("name", ""))
            is_two_prizer = any(tag in name.lower() for tag in (" ex", " v", "vstar", "vmax", "ex"))
            targets.append({
                "slot": "active",
                "id": cid,
                "name": name,
                "prize_yield": 2 if is_two_prizer else 1,
                "hp": game_state.get("opponent_active_hp", 100)
            })

        if isinstance(opp_bench, list):
            for idx, bp in enumerate(opp_bench):
                if isinstance(bp, dict) and bp.get("id"):
                    cid = bp.get("id")
                    card = reg.get_full_skill(cid)
                    name = getattr(card, "card_name", "") if card else str(bp.get("name", ""))
                    is_two_prizer = any(tag in name.lower() for tag in (" ex", " v", "vstar", "vmax", "ex"))
                    targets.append({
                        "slot": f"bench_{idx}",
                        "id": cid,
                        "name": name,
                        "prize_yield": 2 if is_two_prizer else 1,
                        "hp": bp.get("hp", 100)
                    })

        two_prizers = [t for t in targets if t["prize_yield"] == 2]
        one_prizers = [t for t in targets if t["prize_yield"] == 1]

        # Calculate optimal path
        # If remaining prizes == 2 and there's a 2-prizer on bench, Boss it!
        # If remaining prizes == 4 and there are two 2-prizers, ignore 1-prizers!
        preferred_target_slot = None
        boss_boost = 0.0

        if my_prizes_remaining <= 2 and two_prizers:
            # 1 KO on any 2-prizer wins the game instantly
            target = two_prizers[0]
            preferred_target_slot = target["slot"]
            boss_boost = 25.0  # Game-winning Boss's Orders
        elif my_prizes_remaining <= 4 and len(two_prizers) >= 2:
            # Two 2-prizers complete the game (2 + 2 = 4)
            benched_two = [t for t in two_prizers if t["slot"] != "active"]
            if benched_two:
                preferred_target_slot = benched_two[0]["slot"]
                boss_boost = 18.0

        return {
            "my_prizes_remaining": my_prizes_remaining,
            "two_prizer_count": len(two_prizers),
            "one_prizer_count": len(one_prizers),
            "preferred_target_slot": preferred_target_slot,
            "boss_priority_boost": boss_boost
        }
