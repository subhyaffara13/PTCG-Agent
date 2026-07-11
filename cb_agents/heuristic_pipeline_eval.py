"""
Sub-module: score_action, score_state
Delegates to C++ ptcg_core when available for maximum MCTS rollout speed.
"""

import logging
from cb_agents.card_registry import CardRegistry
from cb_agents.card_types import CardStage

logger = logging.getLogger(__name__)
_registry = CardRegistry()

try:
    import ptcg_core as _ptcg_core  # type: ignore
    _HAS_CPP_SCORE = hasattr(_ptcg_core, "score_action")
except Exception:
    _ptcg_core = None
    _HAS_CPP_SCORE = False


def score_action(action: str, gs: dict, threat: float = 0.0) -> float:
    # Fast-path: delegate to C++ implementation (5-10x faster than Python)
    if _HAS_CPP_SCORE:
        try:
            return float(_ptcg_core.score_action(gs, action))
        except Exception as e:
            logger.debug(f"C++ score_action failed: {e}. Falling back to Python.")
    return _score_action_python(action, gs, threat)


def _score_action_python(action: str, gs: dict, threat: float = 0.0) -> float:
    v = 0.0
    dc = gs.get("my_deck_count", 60)
    opp_dc = gs.get("opponent_deck_count", 60)
    mp = gs.get("my_prizes", 6)
    ahp = gs.get("my_active_hp", 100)
    bn = gs.get("my_bench", [])
    ac = gs.get("my_active_pokemon", {})
    opp_hp = gs.get("opponent_active_hp", 100)
    if action.startswith("attack:"):
        v += 1.2  # Attacks are almost always the best action
        if mp <= 1: v += 1.0  # Game-winning attack
        if mp <= 2: v += 0.3  # Close to winning
        opp_ac = gs.get("opponent_active_pokemon", {})
        if isinstance(ac, dict) and isinstance(opp_ac, dict):
            my_type = ac.get("element_type", "")
            opp_weak = opp_ac.get("weakness", "")
            if my_type and opp_weak and my_type.lower() == opp_weak.lower():
                v += 0.5  # Type advantage
        # Check if we can KO
        if isinstance(ac, dict):
            my_active_id = ac.get("id")
            if my_active_id is not None:
                try:
                    card = _registry.get_full_skill(my_active_id)
                    if card and card.damage_output >= opp_hp:
                        v += 1.5  # KO bonus — this is likely the winning move
                except Exception as e:
                    logger.debug(f"KO check registry error: {e}")
    elif action.startswith("evolve:"):
        v += 0.6
    elif action.startswith("attach_energy:"):
        v += 0.45  # Energy attachment is important for enabling attacks
        
        parts = action.split(":")
        target_id = parts[2] if len(parts) > 2 else ""
        active_id = str(ac.get("id", "")) if isinstance(ac, dict) else ""
        is_to_active = not target_id or target_id == active_id
        
        if is_to_active:
            if isinstance(ac, dict):
                need = 2
                try:
                    e = _registry.get_full_skill(ac.get("id"))
                    if e and e.energy_cost > 0: need = e.energy_cost
                except Exception as e:
                    logger.debug(f"Active pokemon energy cost check error: {e}")
                att = len(ac.get("attached", []) or ac.get("energies", []))
                if att < need:
                    v += 0.35  # Stronger bonus for charging up active
                elif att >= need:
                    an = ac.get("card_name", "").lower()
                    sc = any(sa in an for sa in {"raging bolt", "iron hands", "chien pao", "ceruledge", "garchomp", "roaring moon", "groudon", "kyogre"})
                    nr = ahp <= 50 or gs.get("my_active_status", "") in {"poisoned", "burned", "asleep", "paralyzed"}
                    if not sc and not nr: v -= 0.25  # Stronger penalty for over-charging active
        else:
            # Attaching to bench
            v += 0.1  # Moderate priority for charging bench Pokemon
    elif action.startswith("bench:"):
        if not bn: v += 0.8
        else:
            bs = len(bn)
            if bs < 2: v += 0.4
            elif bs < 3: v += 0.25
            elif bs < 4: v += 0.15
            else: v += 0.05
            pr = gs.get("priority_profile", "aggro_push")
            tol = {"aggro_push": 0.15, "closing": 0.10, "disruption": -0.05, "setup": 0.15, "stall": -0.15}.get(pr, 0.0)
            if bs >= 4 and tol < 0: v += tol * bs * 0.3
            elif bs >= 5 and tol <= 0: v -= 0.4
    elif action.startswith("play_trainer:"):
        v += 0.4
        if dc <= 7:
            tn = action.split(":", 1)[1].lower()
            if any(k in tn for k in {"iono", "judge"}): v += 0.8
            elif any(k in tn for k in {"research", "professor", "carmine", "lillie"}): v -= 2.5
        elif dc <= 20 and dc < opp_dc - 3:
            tn = action.split(":", 1)[1].lower()
            if any(k in tn for k in {"iono", "judge"}): v += 0.4
            elif any(k in tn for k in {"research", "professor", "carmine", "lillie"}): v -= 1.2
        if dc > 30:
            n = action.split(":", 1)[1].lower()
            sk = {"nest ball", "ultra ball", "quick ball", "level ball", "secret box", "mega signal", "team rocket's petrel"}
            if any(s in n for s in sk): v += min(0.25, dc * 0.005)
    elif action.startswith("ability:"):
        tn = action.split(":", 1)[1].lower()
        v += 0.35
        if dc <= 7 and any(d in tn for d in {"colress", "concealed", "draw"}): v -= 2.0
        elif dc <= 20 and dc < opp_dc - 3 and any(d in tn for d in {"colress", "concealed", "draw"}): v -= 0.8
    elif action.startswith("retreat:"):
        v += 0.4 if ahp <= 60 else -0.5
        
        # Heavy penalty if retreating to a useless zero-energy Pokemon when active is healthy
        if ahp > 60:
            try:
                target_idx = -1
                if ":" in action:
                    target_idx = int(action.split(":", 1)[1])
                bench = gs.get("my_bench", [])
                if 0 <= target_idx < len(bench):
                    target_poke = bench[target_idx]
                    if isinstance(target_poke, dict):
                        attached_list = target_poke.get("attached") or target_poke.get("energies") or []
                        target_attached = len(attached_list)
                        if target_attached == 0:
                            v -= 0.8  # Penalty of -1.3 total, which is worse than pass (-1.0)
            except Exception as ex:
                logger.warning(f"Error parsing retreat target: {ex}")
                    
        rsb = gs.get("retreat_score_boost", 0.0)
        if rsb > 0: v += rsb
    elif action == "pass":
        v -= 1.0  # Strongly discourage passing
    hs = len(gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else 0
    if hs >= 2 and dc > 10: v += 0.03 * min(hs, 5)
    return v


def score_state(gs: dict) -> float:
    if _HAS_CPP_SCORE:
        try:
            return float(_ptcg_core.score_state(gs))
        except Exception as e:
            logger.debug(f"C++ score_state failed: {e}. Falling back to Python.")
    v = 0.0
    v += 0.15 * (gs.get("opponent_prizes", 6) - gs.get("my_prizes", 6))
    v += 0.001 * (gs.get("my_active_hp", 100) - gs.get("opponent_active_hp", 100))
    all_p = gs.get("my_bench", []) + ([gs.get("my_active_pokemon", {})] if isinstance(gs.get("my_active_pokemon"), dict) and gs.get("my_active_pokemon") else [])
    ec = 0
    for p in all_p:
        if isinstance(p, dict) and p.get("id"):
            try:
                ce = _registry.get(p["id"])
                if ce and ce.stage in (CardStage.STAGE1, CardStage.STAGE2): ec += 1
            except Exception as e:
                logger.debug(f"Stage evolution registry check error: {e}")
    v += 0.05 * ec
    return v
