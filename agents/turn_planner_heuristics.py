"""
agents/turn_planner_heuristics.py
Helper heuristics for TurnPlanner: MCTS bypass checks and action sorting order.
"""
from typing import List

def check_mcts_bypass(candidates: List[str], game_state: dict, rules: dict) -> str:
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

    active = game_state.get("my_active_pokemon") or {}
    active_attached = len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0

    def get_priority_rank(action: str) -> tuple:
        cat_rank = len(order)
        for rank, prefix in enumerate(order):
            if action.startswith(prefix):
                cat_rank = rank
                break

        micro_rank = 0
        if action.startswith("play_trainer:"):
            trainer_name = action.split(":", 1)[1]
            if "Research" in trainer_name or "Professor" in trainer_name or "Iono" in trainer_name:
                has_search = any("ball" in c.lower() for c in candidates)
                micro_rank = 3 if has_search else 1
            elif "Ball" in trainer_name:
                micro_rank = -4
        elif action.startswith("bench:"):
            bench_size = len(game_state.get("my_bench", []))
            if bench_size >= 3:
                micro_rank = 3
        elif action.startswith("attach_energy:"):
            target = action.split(":", 1)[1].lower()
            needed = 3
            act_id = active.get("id") or active.get("card_id") if isinstance(active, dict) else None
            if act_id:
                try:
                    from agents.card_registry import CardRegistry
                    card = CardRegistry().get_full_skill(act_id)
                    if card and card.energy_cost > 0:
                        needed = card.energy_cost
                except:
                    pass
            if "active" in target and active_attached >= needed:
                cat_rank = order.index("attack:") + 1 if "attack:" in order else len(order)
                micro_rank = 10
            elif "bench" in target:
                hp = game_state.get("my_active_hp", 100)
                micro_rank = -5 if (hp <= 50 or active_attached >= needed) else -2

        return (cat_rank, micro_rank, action)

    return sorted(candidates, key=get_priority_rank)
