import logging
import json
from typing import List
from pathlib import Path
from cb_agents.turn_planner_heuristics import _registry
from cb_agents.constants import SCALING_ATTACKERS
from cb_agents.heuristic_pipeline import _dead_weight_heuristic

logger = logging.getLogger(__name__)
_evo_cache = {}

# Load priority_rules.json for strategic action ordering overrides
_PRIORITY_RULES = []
try:
    for _pr_path in [Path("skills/priority_rules.json"), Path(__file__).resolve().parent.parent / "skills" / "priority_rules.json"]:
        if _pr_path.exists():
            _pr_data = json.loads(_pr_path.read_text(encoding="utf-8"))
            _PRIORITY_RULES = _pr_data.get("rules", [])
            break
except Exception:
    pass

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
            "setup": ["bench:", "evolve:", "play_trainer:", "ability:", "attach_energy:", "retreat:", "attack:", "pass"],
            "aggro_push": ["attach_energy:", "bench:", "evolve:", "play_trainer:", "ability:", "attack:", "retreat:", "pass"],
            "disruption": ["play_trainer:", "ability:", "attach_energy:", "bench:", "evolve:", "retreat:", "attack:", "pass"],
            "stall": ["retreat:", "ability:", "play_trainer:", "attach_energy:", "bench:", "evolve:", "pass", "attack:"],
            "closing": ["attack:", "play_trainer:", "ability:", "attach_energy:", "evolve:", "bench:", "retreat:", "pass"],
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
            
            # Apply priority_rules.json overrides for high-impact strategic patterns
            if _PRIORITY_RULES:
                action_lower = action.lower()
                # Boss KO engine rule: if Boss's Orders can KO opponent's engine, max priority
                if action.startswith("play_trainer:") and "boss" in action_lower:
                    opp_bench = game_state.get("opponent_bench", [])
                    engine_names = {"bibarel", "baxcalibur", "pidgeot", "kirlia", "gardevoir"}
                    has_engine_target = any(
                        isinstance(bp, dict) and any(en in str(bp.get("card_name", "")).lower() for en in engine_names)
                        for bp in opp_bench
                    ) if isinstance(opp_bench, list) else False
                    if has_engine_target:
                        micro_rank -= 20  # Highest priority: KO opponent's engine
            
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
                elif any(k in name for k in {"Research", "Professor", "Iono", "Carmine", "Lillie", "Colress"}):
                    dc = game_state.get("my_deck_count", 60)
                    opp_dc = game_state.get("opponent_deck_count", 60)
                    if dc <= 3:
                        micro_rank += 200  # Massive penalty to prevent self-deckout
                    elif dc <= 5 and not any(k in name for k in {"Iono", "Judge"}):
                        micro_rank += 100  # Heavy penalty
                    elif dc <= 7 and not any(k in name for k in {"Iono", "Judge"}):
                        micro_rank += 25  # Moderate penalty
                    elif dc <= 20 and dc < opp_dc - 3 and not any(k in name for k in {"Iono", "Judge"}):
                        micro_rank += 12  # Moderate penalty to conserve deck size when running lower than opponent
                    else:
                        micro_rank -= 5
                # Mill pursuit & Hand-Lock Disruption: smart Iono/Judge timing
                is_iono_judge = any(k in name for k in {"Iono", "Judge"})
                if is_iono_judge:
                    dc = game_state.get("my_deck_count", 60)
                    opp_dc = game_state.get("opponent_deck_count", 60)
                    opp_searched = game_state.get("opponent_searched_last_turn", False)
                    opp_passed_empty = game_state.get("opponent_passed_empty_last_turn", False)
                    
                    opp_prizes = game_state.get("opponent_prizes", 6)
                    opp_hand_count = game_state.get("opponent_hand_count", 0)
                    
                    if opp_prizes <= 2 and opp_hand_count >= 4:
                        micro_rank -= 30  # CRITICAL HAND-LOCK: Opponent is near victory with large hand — shrink hand to 1-2 cards!
                    elif opp_searched:
                        micro_rank -= 15  # Disrupt opponent after they searched for a winning piece
                    elif opp_passed_empty:
                        micro_rank += 25  # PENALTY: Opponent is hand-locked/bricked — don't give them fresh cards!
                    elif opp_dc < dc and opp_dc < 12:
                        micro_rank -= 15  # Accelerate opponent's deck-out
                    elif opp_dc < 8:
                        micro_rank += 50  # Avoid giving opponent cards when near deckout
                        micro_rank -= 10  # Still valuable to shrink opponent deck
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
                    from preference_maps import get_energy_preference  # type: ignore
                    
                preferred_energy = get_energy_preference(target_id)
                if target_id and preferred_energy:
                    if preferred_energy != energy_card:
                        micro_rank = 25  # High penalty for wrong color
                
                is_active_target = False
                if target_id:
                    target_id_str = target_id.lower()
                    active_id = str(active.get("id", "")).lower()
                    if target_id_str in ("active", "my_active_pokemon") or (active_id and target_id_str == active_id):
                        is_active_target = True
                
                if is_active_target:
                    # Determine how much energy active actually needs from card metadata
                    needed = 3
                    try:
                        if isinstance(active, dict):
                            active_card_id = active.get("id")
                            if active_card_id is not None:
                                c = _registry.get_full_skill(active_card_id)
                                if c and c.energy_cost > 0:
                                    needed = c.energy_cost
                    except Exception:
                        pass
                    hp = game_state.get("my_active_hp", 100)
                    if hp <= 50 or active_attached >= needed:
                        micro_rank += 40  # Active is dying or fully charged, heavy penalty for attaching more to it!
                    elif active_attached == 0:
                        micro_rank -= 2
                    else:
                        micro_rank -= 1
                else:
                    # Attaching to bench
                    bench_penalty = -3
                    try:
                        if len(parts) > 2:  # Forward-model format: attach_energy:<energy>:<pokemon_id>
                            poke_id = target_id
                            for bp in game_state.get("my_bench", []):
                                if isinstance(bp, dict) and str(bp.get("id", "")) == poke_id:
                                    bench_att = len(bp.get("attached", []) or bp.get("energies", []))
                                    bp_card = _registry.get_full_skill(poke_id)
                                    if bp_card and bp_card.energy_cost > 0 and bench_att >= bp_card.energy_cost:
                                        bench_penalty = 15  # Over-charging bench penalty
                                    break
                    except Exception:
                        pass
                    micro_rank += bench_penalty
                    
            elif action.startswith("evolve:"):
                micro_rank -= 8
                
            elif action.startswith("retreat:"):
                # Penalize retreat by default to rank it below passing, unless we have a specific reason
                retreat_penalty = 35  # Heavily penalize by default to put it below pass (which is rank 55)
                
                # Check if we have defensive retreat boost
                boost = game_state.get("retreat_score_boost", 0.0)
                if boost > 0:
                    retreat_penalty = -5
                else:
                    # Let's inspect target and active to see if it makes sense
                    hp = game_state.get("my_active_hp", 100)
                    if hp <= 40:
                        # Active is close to KO, retreating is reasonable if we have another Pokemon
                        retreat_penalty = 5
                    else:
                        # Active is healthy. Check if active has energy that would be discarded
                        active_energy_count = len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0
                        if active_energy_count == 0:
                            # 0 energy retreat is free, no energy lost
                            retreat_penalty = 0
                micro_rank += retreat_penalty
                
            elif action == "pass":
                dc = game_state.get("my_deck_count", 60)
                opp_dc = game_state.get("opponent_deck_count", 60)
                if opp_dc < dc and opp_dc < 8:
                    micro_rank -= 12  # Stall: passing lets opponent draw closer to deck-out
                else:
                    micro_rank += 20
                
            # Blend Neural Prior
            prior = neural_priors.get(action, 0.0)
            # Subtracting from rank increases priority. A strong prior (e.g. 0.8) subtracts up to 16 from rank.
            neural_bonus = prior * 20.0
            
            return cat_rank * 15 + micro_rank - neural_bonus

        return sorted(candidates, key=get_priority_rank)
    except Exception as e:
        logger.error(f"sort_actions_heuristically failed: {e}", exc_info=True)
        return candidates
