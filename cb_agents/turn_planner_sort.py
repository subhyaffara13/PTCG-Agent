import logging
from typing import List
from cb_agents.turn_planner_heuristics import _registry, _SCALING_ATTACKERS
from cb_agents.heuristic_pipeline import _dead_weight_heuristic

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

_nn_instance = None
def _get_neural_network():
    global _nn_instance
    if _nn_instance is None:
        try:
            from cb_agents.value_network import NeuralValueNetwork
            _nn_instance = NeuralValueNetwork()
        except Exception as e:
            logger.warning(f"Failed to instantiate NeuralValueNetwork: {e}")
    return _nn_instance

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
        
        # 1. Fetch Neural Priors
        neural_priors = {}
        nn = _get_neural_network()
        if nn is not None:
            try:
                neural_priors = nn.get_action_priors(game_state, candidates)
            except Exception as e:
                logger.warning(f"Failed to fetch neural priors: {e}")

        def get_priority_rank(action: str) -> tuple:
            cat_rank = len(order)
            for rank, prefix in enumerate(order):
                if action.startswith(prefix):
                    cat_rank = rank
                    break
            micro_rank = 0
            
            # Combo tag priority logic
            card_id = None
            if ":" in action:
                parts = action.split(":", 2)
                card_id = parts[1]
                if card_id.isdigit():
                    try:
                        c = _registry.get(int(card_id))
                        if c and c.combo_tags:
                            if profile == "setup" and any(t in ("search", "bench", "setup") for t in c.combo_tags):
                                micro_rank -= 4
                            elif profile in ("aggro_push", "closing") and any(t in ("damage", "discard", "boss") for t in c.combo_tags):
                                micro_rank -= 4
                    except Exception:
                        pass
                        
            if action.startswith("play_trainer:"):
                name = action.split(":", 1)[1]
                has_dead = _dead_weight_heuristic(candidates, game_state)
                _discard_search = {"ultra ball", "earthen vessel"}
                if has_dead and any(ds in name.lower() for ds in _discard_search):
                    micro_rank -= 6
                elif "Research" in name or "Professor" in name or "Iono" in name:
                    micro_rank -= 5
                elif "Ball" in name:
                    micro_rank -= 1
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
                parts = action.split(":")
                energy_card = parts[1] if len(parts) > 1 else ""
                target_id = parts[2] if len(parts) > 2 else (parts[1] if len(parts) == 2 else "")
                
                try:
                    from cb_agents.preference_maps import get_energy_preference
                except ImportError:
                    from cb_agents.preference_maps import get_energy_preference
                    
                preferred_energy = get_energy_preference(target_id)
                if target_id and preferred_energy:
                    if preferred_energy != energy_card:
                        micro_rank = 25  # High penalty for wrong color
                
                is_active_target = False
                if target_id:
                    target_id_str = str(target_id).lower()
                    active_id = str(active.get("id", "")).lower()
                    if target_id_str in ("active", "my_active_pokemon") or (active_id and target_id_str == active_id):
                        is_active_target = True
                
                if is_active_target:
                    # Determine how much energy active actually needs
                    needed = 3
                    hp = game_state.get("my_active_hp", 100)
                    if hp <= 50 or active_attached >= needed:
                        micro_rank += 20  # Active is dying or fully charged, heavy penalty for attaching more to it!
                    elif active_attached == 0:
                        micro_rank -= 2
                    else:
                        micro_rank -= 1
                else:
                    # Attaching to bench
                    micro_rank -= 3
                    
            elif action.startswith("evolve:"):
                micro_rank -= 8
                
            elif action.startswith("attack:"):
                micro_rank -= 10
                
            elif action == "pass":
                micro_rank += 20
                
            # Blend Neural Prior
            prior = neural_priors.get(action, 0.0)
            # Subtracting from rank increases priority. A strong prior (e.g. 0.8) subtracts up to 16 from rank.
            neural_bonus = prior * 20.0
            
            return cat_rank * 5 + micro_rank - neural_bonus

        return sorted(candidates, key=get_priority_rank)
    except Exception as e:
        logger.error(f"sort_actions_heuristically failed: {e}", exc_info=True)
        return candidates
