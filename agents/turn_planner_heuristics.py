"""
agents/turn_planner_heuristics.py

Helper heuristics for TurnPlanner: MCTS bypass checks and action sorting order.
"""

from typing import List, Dict, Any

def check_mcts_bypass(candidates: List[str], game_state: dict, rules: dict) -> str:
    """
    Bypasses MCTS for non-deterministic draw/search actions to guarantee perfect sequencing.
    """
    my_deck_count = game_state.get("my_deck_count", 60)
    
    priority_keywords = [
        "nest ball", "ultra ball", "research", "iono", "judge", "concealed cards", 
        "flower selecting", "shining arcana", "colress", "quick ball", "level ball",
        "secret box", "mega signal", "team rocket's petrel", "surfing beach"
    ]
    draw_keywords = {"research", "iono", "judge", "concealed cards", "flower selecting", "shining arcana", "colress"}
    
    for cand in candidates:
        if cand.startswith("play_trainer:") or cand.startswith("attack:") or cand.startswith("ability:"):
            target = cand.split(":")[1].lower()
            
            if my_deck_count <= 5 and any(dk in target for dk in draw_keywords):
                continue
                
            for keyword in priority_keywords:
                if keyword in target:
                    return cand
                    
    for rule in rules.get("rules", []):
        if rule.get("action") == "PLAY_SUPPORTER_BOSS":
            for cand in candidates:
                if cand.startswith("play_trainer:boss"):
                    return cand
    return None

def sort_actions_heuristically(candidates: List[str], profile: str, game_state: dict) -> List[str]:
    """Sorts actions based on the explicit priority order per profile."""
    profile_orders = {
        "aggro_push": ["evolve:", "attach_energy:", "play_trainer:", "bench:", "retreat:", "attack:", "pass"],
        "setup": ["bench:", "play_trainer:", "retreat:", "attach_energy:", "evolve:", "attack:", "pass"],
        "disruption": ["play_trainer:", "retreat:", "bench:", "attach_energy:", "evolve:", "attack:", "pass"],
        "stall": ["play_trainer:", "retreat:", "bench:", "attach_energy:", "evolve:", "attack:", "pass"],
        "closing": ["retreat:", "attach_energy:", "attack:", "evolve:", "play_trainer:", "bench:", "pass"]
    }

    order = profile_orders.get(profile, profile_orders["aggro_push"])
    
    if "my_bench" in game_state and not game_state["my_bench"]:
        order = ["bench:", "play_trainer:", "evolve:", "attach_energy:", "retreat:", "attack:", "pass"]

    active_pokemon = game_state.get("my_active_pokemon")
    over_attached = False
    if isinstance(active_pokemon, dict):
        card_id = active_pokemon.get("id")
        attached_list = active_pokemon.get("attached") or active_pokemon.get("energies", [])
        attached_count = len(attached_list)
        try:
            from agents.card_registry import CardRegistry
            registry = CardRegistry()
            card_entry = registry.get_full_skill(card_id)
            needed = card_entry.energy_cost if card_entry else 3
        except Exception:
            needed = 3 if card_id == 722 else 2
        if attached_count >= needed:
            over_attached = True

    def get_priority_rank(action: str) -> tuple:
        cat_rank = len(order)
        for rank, prefix in enumerate(order):
            if action.startswith(prefix):
                cat_rank = rank
                break

        micro_rank = 0
        if action.startswith("play_trainer:"):
            trainer_name = action.split(":", 1)[1]
            if "Research" in trainer_name or "Professor" in trainer_name:
                micro_rank = -2
            elif "Ball" in trainer_name:
                micro_rank = 2
        elif action.startswith("attach_energy:"):
            if over_attached:
                cat_rank = order.index("pass") - 1
                micro_rank = 10

        return (cat_rank, micro_rank, action)

    return sorted(candidates, key=get_priority_rank)
