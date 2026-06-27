import logging
from typing import List
from agents.turn_planner_heuristics import _registry, _SCALING_ATTACKERS
from agents.heuristic_pipeline import _dead_weight_heuristic

logger = logging.getLogger(__name__)
_evo_cache = {}

def _has_evolution_target(card_name: str, decklist: dict) -> bool:
    k = (card_name, frozenset(decklist.keys()))
    if k in _evo_cache: return _evo_cache[k]
    try:
        cn = card_name.split("(")[0].strip()
        for cid in decklist:
            c = _registry.get(int(cid))
            if c and c.previous_stage and cn in c.previous_stage.lower():
                _evo_cache[k] = True; return True
        _evo_cache[k] = False; return False
    except:
        return True

_EARLY_BENCH_ORDER = ["play_trainer:", "ability:", "bench:", "retreat:", "attack:", "evolve:", "attach_energy:", "pass"]

def sort_actions_heuristically(candidates: List[str], profile: str, game_state: dict) -> List[str]:
    try:
        profile_orders = {
            "setup": ["bench:", "evolve:", "attach_energy:", "play_trainer:", "ability:", "retreat:", "attack:", "pass"],
            "aggro_push": ["bench:", "evolve:", "attach_energy:", "play_trainer:", "ability:", "retreat:", "attack:", "pass"],
            "disruption": ["play_trainer:", "ability:", "retreat:", "attack:", "bench:", "evolve:", "attach_energy:", "pass"],
            "stall": ["play_trainer:", "ability:", "retreat:", "attack:", "bench:", "evolve:", "attach_energy:", "pass"],
            "closing": ["play_trainer:", "ability:", "retreat:", "attack:", "bench:", "evolve:", "attach_energy:", "pass"],
        }
        order = profile_orders.get(profile, profile_orders["aggro_push"])
        if "my_bench" in game_state and not game_state["my_bench"]:
            order = _EARLY_BENCH_ORDER

        active = game_state.get("my_active_pokemon") or {}
        active_attached = len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0
        bench_size = len(game_state.get("my_bench", []))
        my_hand_size = len(game_state.get("my_hand", []))

        def get_priority_rank(action: str) -> tuple:
            cat_rank = len(order)
            for rank, prefix in enumerate(order):
                if action.startswith(prefix):
                    cat_rank = rank
                    break
            micro_rank = 0
            if action.startswith("play_trainer:"):
                name = action.split(":", 1)[1]
                has_dead = _dead_weight_heuristic(candidates, game_state)
                _discard_search = {"ultra ball", "earthen vessel"}
                if has_dead and any(ds in name.lower() for ds in _discard_search):
                    micro_rank = -6
                elif "Research" in name or "Professor" in name or "Iono" in name:
                    micro_rank = -5
                elif "Ball" in name:
                    micro_rank = 1
            elif action.startswith("bench:"):
                bench_need = 0
                if profile == "setup":
                    bench_need = 5
                elif profile in ("aggro_push", "closing"):
                    bench_need = 2
                if bench_size >= bench_need:
                    micro_rank = 5
                elif my_hand_size < 3 and bench_size == 0:
                    micro_rank = -3
            elif action.startswith("attach_energy:"):
                target = action.split(":", 1)[1].lower()
                needed = 3
                act_id = active.get("id") or active.get("card_id") if isinstance(active, dict) else None
                if act_id:
                    try:
                        card = _registry.get_full_skill(act_id)
                        if card and card.energy_cost > 0:
                            needed = card.energy_cost
                    except ImportError:
                        pass
                if "active" in target and active_attached >= needed:
                    act_name = active.get("card_name", "").lower() if isinstance(active, dict) else ""
                    is_scaling = any(sa in act_name for sa in _SCALING_ATTACKERS)
                    if not is_scaling:
                        cat_rank = order.index("attack:") + 1 if "attack:" in order else len(order)
                        micro_rank = 10
                elif "bench" in target:
                    hp = game_state.get("my_active_hp", 100)
                    micro_rank = -5 if (hp <= 50 or active_attached >= needed) else -2
            return cat_rank * 5 + micro_rank

        return sorted(candidates, key=get_priority_rank)
    except Exception as e:
        logger.error(f"sort_actions_heuristically failed: {e}", exc_info=True)
        return candidates
