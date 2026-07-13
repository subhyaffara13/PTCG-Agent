"""
Sub-module: score_action, score_state
Delegates to C++ ptcg_core when available for maximum MCTS rollout speed.
"""

import logging
from cb_agents.card_registry import CardRegistry
from cb_agents.card_types import CardStage

logger = logging.getLogger(__name__)
_registry = CardRegistry()

from cb_agents.card_utils import _get_prize_yield

try:
    import ptcg_core as _ptcg_core  # type: ignore
except Exception:
    _ptcg_core = None
# Force Python scoring: C++ score_action is stale (missing retreat better-attacker,
# hand-size-aware supporters, one-short energy bonus, bench evolution scoring).
# The C++ MCTS engine uses its own internal scoring (unaffected).
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
        # Check if attack is actually feasible: active must have enough energy
        # Also check if we are paralyzed or asleep (can't attack)
        my_status = gs.get("my_active_status", "")
        is_stunned = my_status in ("paralyzed", "asleep")
        can_attack = not is_stunned
        if isinstance(ac, dict) and not is_stunned:
            attached_count = len(ac.get("attached", []) or ac.get("energies", []))
            active_id = ac.get("id")
            if active_id is not None:
                try:
                    min_cost = _registry.get_min_energy_cost(active_id)
                    can_attack = attached_count >= min_cost
                except Exception:
                    can_attack = attached_count >= 1
            else:
                can_attack = attached_count >= 1
        if not can_attack:
            v -= 0.5 if not is_stunned else 0.8  # Extra penalty if stunned
        else:
            v += 0.65  # Attacks are good when actually usable
        # Poison/burn tick damage: prefer attacking sooner
        if my_status in ("poisoned", "burned"):
            v += 0.2  # Push to attack before tick damage KOs us
        if mp <= 1: v += 1.0  # Game-winning attack
        if mp <= 2: v += 0.3  # Close to winning
        opp_ac = gs.get("opponent_active_pokemon", {})
        if isinstance(ac, dict) and isinstance(opp_ac, dict):
            my_type = ac.get("element_type", "")
            opp_weak = opp_ac.get("weakness", "")
            if my_type and opp_weak and my_type.lower() == opp_weak.lower():
                v += 0.5  # Type advantage
        # Check if we can KO
        if isinstance(ac, dict) and not is_stunned:
            my_active_id = ac.get("id")
            if my_active_id is not None:
                try:
                    card = _registry.get_full_skill(my_active_id)
                    if card and card.damage_output >= opp_hp:
                        v += 1.5  # KO bonus — this is likely the winning move
                except Exception as e:
                    logger.debug(f"KO check registry error: {e}")
        # Opponent status awareness: bonus if opponent is asleep/paralyzed (can't attack back)
        opp_status = gs.get("opponent_active_status", "")
        if opp_status in ("asleep", "paralyzed"):
            v += 0.4  # Free hit — opponent can't retaliate
        elif opp_status in ("poisoned", "burned", "confused"):
            v += 0.15  # Slight edge: opponent is weakened
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
                    if att == need - 1:
                        v += 0.2  # Extra bonus when one short of attack
                elif att >= need:
                    an = ac.get("card_name", "").lower()
                    sc = any(sa in an for sa in {"raging bolt", "iron hands", "chien pao", "ceruledge", "garchomp", "roaring moon", "groudon", "kyogre"})
                    nr = ahp <= 50 or gs.get("my_active_status", "") in {"poisoned", "burned", "asleep", "paralyzed"}
                    if not sc and not nr: v -= 0.25  # Stronger penalty for over-charging active
        else:
            # Attaching to bench
            v += 0.1  # Moderate priority for charging bench Pokemon
            # Check if the target bench Pokemon already has enough energy
            if len(parts) > 2:
                try:
                    poke_id = parts[2]
                    for bp in bn:
                        if isinstance(bp, dict) and str(bp.get("id", "")) == poke_id:
                            bench_att = len(bp.get("attached", []) or bp.get("energies", []))
                            bp_card = _registry.get_full_skill(poke_id)
                            if bp_card and bp_card.energy_cost > 0:
                                if bench_att < bp_card.energy_cost:
                                    v += 0.2  # Charging up bench attacker
                                    if bench_att == bp_card.energy_cost - 1:
                                        v += 0.2  # One short of attacking
                                else:
                                    v -= 0.3  # Penalty for over-charging bench
                            break
                except Exception:
                    pass
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
        try:
            bench_parts = action.split(":")
            bench_card_id = int(bench_parts[1]) if len(bench_parts) > 1 and bench_parts[1].isdigit() else None
            if bench_card_id is not None:
                bc = _registry.get_full_skill(bench_card_id)
                if bc:
                    if bc.stage in (CardStage.STAGE1, CardStage.STAGE2):
                        v += 0.2  # Evolution fodder is valuable
                    if bc.hp and bc.hp > 120:
                        v += 0.1  # Tanky basics
                    # Prize denial: penalize benching high-prize Pokemon when bench already has one
                    py = _get_prize_yield(bc.card_name)
                    if py >= 2:
                        # How many high-prize Pokemon already on board?
                        high_prize_count = 1 if _get_prize_yield(str(ac.get("card_name", "") if isinstance(ac, dict) else "")) >= 2 else 0
                        for bp in bn:
                            if isinstance(bp, dict):
                                hp_name = bp.get("card_name", "")
                                if _get_prize_yield(str(hp_name)) >= 2:
                                    high_prize_count += 1
                        if high_prize_count >= 1:
                            penalty = 0.3 * py
                            # Amplify penalty if opponent likely has Boss's Orders
                            boss_prob = gs.get("boss_prob", 0.0)
                            if boss_prob > 0.3:
                                penalty *= min(3.0, 1.0 + boss_prob * 2.0)
                            v -= penalty
        except Exception:
            pass
    elif action.startswith("play_trainer:"):
        v += 0.4
        hs = len(gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else 0
        if dc <= 7:
            tn = action.split(":", 1)[1].lower()
            if any(k in tn for k in {"iono", "judge"}): v -= 2.5  # Iono can deck you out from 7
            elif any(k in tn for k in {"research", "professor", "carmine", "lillie"}): v -= 2.5
        elif dc <= 20 and dc < opp_dc - 3:
            tn = action.split(":", 1)[1].lower()
            if any(k in tn for k in {"research", "professor", "carmine", "lillie"}): v -= 1.2
        if dc > 30:
            n = action.split(":", 1)[1].lower()
            sk = {"nest ball", "ultra ball", "quick ball", "level ball", "secret box", "mega signal", "team rocket's petrel"}
            if any(s in n for s in sk): v += min(0.25, dc * 0.005)
        # Hand-size-aware draw supporter valuation
        if hs > 5 and dc > 10:
            tn = action.split(":", 1)[1].lower()
            if any(k in tn for k in {"iono", "judge"}):
                v += min(0.6, hs * 0.08)  # Big hand -> big shuffle value (draws up to hand-size cards)
            if any(k in tn for k in {"research", "professor", "carmine"}):
                v += min(0.4, hs * 0.05)  # Big hand -> more cards to discard with Research
    elif action.startswith("ability:"):
        tn = action.split(":", 1)[1].lower()
        v += 0.35
        if dc <= 7 and any(d in tn for d in {"colress", "concealed", "draw"}): v -= 2.0
        elif dc <= 20 and dc < opp_dc - 3 and any(d in tn for d in {"colress", "concealed", "draw"}): v -= 0.8
    elif action.startswith("retreat:"):
        v += 0.4 if ahp <= 60 else -0.5
        
        # Reward switching to a better attacker instead of blanket penalty
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
                    target_id = target_poke.get("id")
                    if target_id is not None:
                        tc = _registry.get_full_skill(target_id)
                        is_better_attacker = tc and tc.damage_output > 0 and target_attached >= max(1, tc.energy_cost)
                        if is_better_attacker:
                            v += 0.8  # Switching to a usable attacker is great
                        elif target_attached == 0:
                            v -= 0.8  # Penalty for zero-energy swap
        except Exception as ex:
            logger.warning(f"Error parsing retreat target: {ex}")
                    
        rsb = gs.get("retreat_score_boost", 0.0)
        if rsb > 0: v += rsb
    elif action == "pass":
        v -= 1.0  # Strongly discourage passing
    # Prefer attacking over drawing when near deck-out
    if dc <= 8 and opp_hp > 0:
        if action.startswith("play_trainer:"):
            tn = action.split(":", 1)[1].lower()
            if any(k in tn for k in {"research", "professor", "carmine", "lillie", "iono", "judge"}):
                v -= 1.0  # Draw supporter when opponent is alive — risk deck-out
        elif action.startswith("ability:"):
            tn = action.split(":", 1)[1].lower()
            if any(d in tn for d in {"colress", "concealed", "draw"}):
                v -= 1.0  # Draw ability when opponent is alive — risk deck-out
    hs = len(gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else 0
    if hs >= 2 and dc > 10: v += 0.03 * min(hs, 5)

    # Deck-out race pursuit: actively mill opponent when we have more deck remaining
    _avg_draw = 1.5
    my_turns_left = dc / _avg_draw if dc > 0 else 0
    opp_turns_left = opp_dc / _avg_draw if opp_dc > 0 else 0
    we_outlast = my_turns_left > opp_turns_left + 1
    if action.startswith("play_trainer:"):
        tn = action.split(":", 1)[1].lower()
        is_shuffle = any(k in tn for k in {"iono", "judge"})
        is_draw = any(k in tn for k in {"research", "professor", "carmine", "lillie"})
        if (opp_dc < dc or (opp_dc < 10 and we_outlast)) and is_shuffle:
            v += 1.2  # Shuffle-mill accelerates opponent deck-out
        elif opp_dc < 8 and we_outlast:
            if is_draw:
                v -= 0.8  # Don't draw when opponent is nearly out — let them draw first
            if "pass" in action or any(k in tn for k in {"potion", "heal", "switch", "scoop"}):
                v += 0.6  # Stall to let opponent draw out
    elif action in ("pass",) and opp_dc < 10 and we_outlast:
        v += 0.8  # Passing is good when opponent will deck out before us
    elif action.startswith("retreat:") and opp_dc < 10 and we_outlast:
        v += 0.4  # Retreating to a tanky Pokemon also stalls
    elif action.startswith("ability:"):
        tn = action.split(":", 1)[1].lower()
        if opp_dc < 10 and we_outlast and any(d in tn for d in {"heal", "protect", "barrier"}):
            v += 0.5  # Stall abilities help survive until opponent decks out

    # Inject learned_dos / learned_donts into action scoring
    try:
        cid = None
        if action.startswith("bench:"):
            parts = action.split(":")
            if len(parts) > 1 and parts[1].lstrip("-").isdigit():
                cid = int(parts[1])
        elif action.startswith("evolve:"):
            parts = action.split(":")
            if len(parts) > 2 and parts[2].lstrip("-").isdigit():
                cid = int(parts[2])
        elif action.startswith("play_trainer:"):
            tn = action.split(":", 1)[1].lower()
            for store_id, store_card in getattr(_registry, "cards", {}).items():
                if store_card.card_name.lower() == tn:
                    cid = int(store_id) if not isinstance(store_id, int) else store_id
                    break
        if cid is not None:
            dos = getattr(_registry, "learned_dos", set())
            donts = getattr(_registry, "learned_donts", set())
            if cid in dos:
                v += 0.5
            if cid in donts:
                v -= 0.5
    except Exception:
        pass
    return v


def score_state(gs: dict) -> float:
    if _HAS_CPP_SCORE:
        try:
            return float(_ptcg_core.score_state(gs))
        except Exception as e:
            logger.debug(f"C++ score_state failed: {e}. Falling back to Python.")
    v = 0.0
    mp = gs.get("my_prizes", 6)
    opp_p = gs.get("opponent_prizes", 6)
    turn = gs.get("turn_number", 1)
    v += 0.15 * (opp_p - mp)
    v += 0.001 * (gs.get("my_active_hp", 100) - gs.get("opponent_active_hp", 100))
    
    # Turn-number awareness: early game favors setup, late game favors aggression
    if turn <= 3:
        v += 0.1  # Early game: slightly positive for having drawn well
    elif turn >= 10:
        v += 0.2 * (gs.get("my_bench_count", 0) >= 3)  # Late game: reward board presence
    
    # KO-threat awareness: penalize if opponent can KO our active
    opp_damage = gs.get("_projected_opponent_damage", None)
    if opp_damage is None:
        # Compute inline using registry if not prefilled
        try:
            opp_active = gs.get("opponent_active_pokemon", gs.get("opponent_active", {}))
            if isinstance(opp_active, dict) and opp_active.get("id"):
                from cb_agents.card_registry import CardRegistry
                reg = CardRegistry()
                oid = int(opp_active["id"]) if not isinstance(opp_active["id"], int) else opp_active["id"]
                ocard = reg.get_full_skill(oid)
                if ocard and ocard.damage_output:
                    opp_att = len(opp_active.get("attached", []) or opp_active.get("energies", []))
                    if opp_att >= max(1, ocard.energy_cost):
                        opp_damage = ocard.damage_output
                        atk_type = reg.card_poke_type.get(oid, "")
                        my_active = gs.get("my_active_pokemon", {})
                        if isinstance(my_active, dict) and my_active.get("id"):
                            my_id = int(my_active["id"]) if not isinstance(my_active["id"], int) else my_active["id"]
                            weak = reg.card_weakness.get(my_id, "")
                            resist = reg.card_resistance.get(my_id, "")
                            if atk_type and weak and atk_type == weak:
                                opp_damage *= 2
                            if atk_type and resist and atk_type == resist:
                                opp_damage = max(0, opp_damage - 30)
        except Exception:
            opp_damage = 0
    else:
        try:
            opp_damage = int(opp_damage)
        except (TypeError, ValueError):
            opp_damage = 0
    my_hp = gs.get("my_active_hp", 100)
    if opp_damage > 0 and opp_damage >= my_hp:
        v -= 0.8  # One-shot lethal threat
    elif opp_damage > 0 and opp_damage >= my_hp * 0.6:
        v -= 0.3  # Significant damage threat
    
    # Status awareness
    my_status = gs.get("my_active_status", "")
    if my_status in ("poisoned", "burned"):
        v -= 0.15  # Tick damage will wear us down
    elif my_status in ("paralyzed", "asleep"):
        v -= 0.3  # Can't act is very bad
    opp_status = gs.get("opponent_active_status", "")
    if opp_status in ("paralyzed", "asleep"):
        v += 0.3  # Opponent can't act
    elif opp_status in ("poisoned", "burned"):
        v += 0.15  # Opponent taking tick damage
    
    # Deck-size awareness: penalize low own deck, reward low opponent deck
    my_dc = gs.get("my_deck_count", 60)
    opp_dc = gs.get("opponent_deck_count", 60)
    if my_dc <= 3:
        v -= 0.5  # Near deck-out panic
    elif my_dc <= 8:
        v -= 0.2
    if opp_dc <= 3:
        v += 0.3  # Opponent near deck-out
    elif opp_dc <= 8:
        v += 0.1

    # Deck-out race comparison: who will deck out first?
    if my_dc > 0 and opp_dc > 0:
        avg_draw = 1.5
        my_turns = my_dc / avg_draw
        opp_turns = opp_dc / avg_draw
        turns_diff = my_turns - opp_turns
        if turns_diff > 3:
            v += 0.4  # We clearly outlast opponent — stalling is winning
            v += 0.05 * min(turns_diff, 8)
        elif turns_diff > 1:
            v += 0.15  # Slight edge in deck-out race
        elif turns_diff < -3:
            v -= 0.4  # Opponent outlasts us — must take prizes fast
        elif turns_diff < -1:
            v -= 0.15  # Slight deficit in deck-out race
    # Turns-until-deckout: estimate remaining turns and penalize critically low
    if my_dc > 0:
        hand_size = len(gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else 0
        avg_draw_per_turn = 1.5  # conservative: draw 1 + occasional supporter
        turns_left = max(0, my_dc / avg_draw_per_turn)
        if turns_left <= 1:
            v -= 0.8  # Will deck out THIS turn
        elif turns_left <= 2:
            v -= 0.4  # 1-2 turns left
        elif turns_left <= 3:
            v -= 0.15  # 2-3 turns left
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
