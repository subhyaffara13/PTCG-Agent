from cb_agents.heuristic_pipeline import pipeline

from cb_agents.card_utils import _get_prize_yield

def _get_opponent_element_type(game_state) -> str:
    """Get the opponent's active Pokemon's element type."""
    try:
        active = getattr(game_state, 'opponent_active', None)
        if isinstance(active, dict):
            return active.get("element_type", "") or active.get("type", "") or ""
    except Exception:
        pass
    return ""

def _get_poke_type_resistance(tc, opp_type: str) -> float:
    """Score type matchup using registry weakness/resistance: +2 resist, -2 weak, 0 neutral."""
    if not opp_type or not tc:
        return 0.0
    try:
        from cb_agents.card_registry import CardRegistry
        registry = CardRegistry()
        card_id = tc.id if hasattr(tc, 'id') else None
        if card_id is None:
            return 0.0
        poke_type = registry.card_poke_type.get(int(card_id), "")
        if not poke_type:
            return 0.0
        # Check if our type resists opponent type (opponent's attack is not very effective)
        weak_against_opp = registry.card_weakness.get(int(card_id), "")
        resist_against_opp = registry.card_resistance.get(int(card_id), "")
        opp_type_lower = opp_type.lower()
        if resist_against_opp and resist_against_opp.lower() == opp_type_lower:
            return 2.0  # We resist
        if weak_against_opp and weak_against_opp.lower() == opp_type_lower:
            return -2.0  # We are weak
    except Exception:
        pass
    return 0.0

def _apply_weakness_resistance(damage: int, atk_type: str, defender_id, registry) -> int:
    """Apply weakness (2x) and resistance (-30) to raw damage."""
    if not atk_type or defender_id is None or damage <= 0:
        return damage
    try:
        def_id = int(defender_id) if not isinstance(defender_id, int) else defender_id
        weak = registry.card_weakness.get(def_id, "")
        resist = registry.card_resistance.get(def_id, "")
        if atk_type and weak and atk_type == weak:
            damage *= 2
        if atk_type and resist and atk_type == resist:
            damage = max(0, damage - 30)
    except Exception:
        pass
    return damage


def project_opponent_damage_helper(game_state) -> dict:
    """Returns dict with 'max_damage', 'can_2hko' (bool), and 'opponent_type' (str)."""
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    result = {"max_damage": 0, "can_2hko": False, "opponent_type": ""}
    active = getattr(game_state, 'opponent_active', None)
    if active:
        try:
            opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
            card = registry.get_full_skill(opp_active_id)
            if card:
                raw_dmg = card.damage_output
                opp_attached = len(active.get("attached", []) or active.get("energies", [])) if isinstance(active, dict) else 0
                if opp_attached < max(1, card.energy_cost):
                    raw_dmg = 0
                # Apply weakness/resistance: opponent's attack type vs our active's type
                if raw_dmg > 0:
                    opp_type = registry.card_poke_type.get(opp_active_id, "")
                    my_active = getattr(game_state, 'my_active_pokemon', None) or {}
                    my_active_id = my_active.get("id") if isinstance(my_active, dict) else None
                    if my_active_id is not None:
                        raw_dmg = _apply_weakness_resistance(raw_dmg, opp_type, my_active_id, registry)
                result["max_damage"] = raw_dmg
                result["opponent_type"] = _get_opponent_element_type(game_state)
                if isinstance(active, dict) and active.get("id") and raw_dmg > 0:
                    my_hp = getattr(game_state, 'my_active_hp', 100)
                    if raw_dmg < my_hp <= raw_dmg * 2:
                        result["can_2hko"] = True
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"project_opponent_damage failed: {e}")
    return result

def _best_retreat_target(retreat_actions, game_state, opponent_max_damage=0, opponent_type=""):
    """Pick the retreat target that balances attack capability, survivability, and type matchup."""
    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    bench = list(getattr(game_state, 'my_bench', []))
    best_action = retreat_actions[0]
    best_score = -999

    # Check opponent's current energy for post-retreat evaluation
    opp_attached_energy = 0
    opp_active = getattr(game_state, 'opponent_active', None)
    if isinstance(opp_active, dict):
        opp_attached_energy = len(opp_active.get("attached", []) or opp_active.get("energies", []))

    for ra in retreat_actions:
        try:
            idx = int(ra.replace("retreat:", "").strip())
            if 0 <= idx < len(bench):
                bp = bench[idx]
                if isinstance(bp, dict):
                    ba = len(bp.get("attached", []) or bp.get("energies", []))
                    bid = bp.get("id")
                    if bid is not None:
                        tc = registry.get_full_skill(bid)
                        if tc:
                            ec = max(1, tc.energy_cost) if tc.energy_cost else 1
                            dmg = tc.damage_output or 0
                            hp = tc.hp or 100
                            score = dmg if ba >= ec else (-10 - idx)
                            # Survivability vs opponent max damage
                            if opponent_max_damage > 0:
                                if hp < opponent_max_damage:
                                    score -= 5.0  # Target dies immediately
                                elif hp <= opponent_max_damage * 1.5:
                                    score -= 1.0  # 2HKO range
                                if hp >= opponent_max_damage * 2:
                                    score += 1.5  # Safe tank
                            # Type resistance/weakness bonus
                            type_score = _get_poke_type_resistance(tc, opponent_type)
                            if type_score != 0.0:
                                score += type_score * 0.5  # +/-1.0 for type matchup
                            # Opponent energy check: can they KO the new active with existing energy?
                            if opp_attached_energy > 0:
                                opp_card = None
                                if isinstance(opp_active, dict):
                                    try:
                                        opp_card = registry.get_full_skill(opp_active.get("id"))
                                    except Exception:
                                        pass
                                if opp_card and opp_attached_energy >= max(1, opp_card.energy_cost):
                                    if opponent_max_damage >= hp:
                                        score -= 3.0  # Opponent already has energy to KO the swap-in
                            if score > best_score:
                                best_score = score
                                best_action = ra
        except Exception:
            pass
    return best_action

def check_defensive_retreat_helper(game_state, board_summary) -> str:
    dmg_info = project_opponent_damage_helper(game_state)
    opponent_max_damage = dmg_info["max_damage"]
    opponent_type = dmg_info.get("opponent_type", "")
    my_hp = getattr(game_state, 'my_active_hp', 0)
    retreat_actions = list(getattr(game_state, 'legal_retreats', []))
    if not retreat_actions:
        return None
    # One-shot lethal: strong retreat push
    if opponent_max_damage > 0 and opponent_max_damage >= my_hp:
        return _best_retreat_target(retreat_actions, game_state, opponent_max_damage, opponent_type)
    # Preemptive 2HKO: softer retreat suggestion (lets other actions compete)
    if dmg_info.get("can_2hko") and my_hp <= opponent_max_damage * 1.8:
        return _best_retreat_target(retreat_actions, game_state, opponent_max_damage, opponent_type)
    return None

def update_opponent_model_helper(orchestrator, game_state):
    from router.bus import OpponentModelPacket
    newly_played = game_state.opponent_revealed if game_state.opponent_revealed else []
    orchestrator.bus.dispatch("OpponentModel", OpponentModelPacket(
        turn=orchestrator.current_turn, newly_played_cards=newly_played,
        revealed_active_pokemon=game_state.opponent_active,
        revealed_bench_count=len(game_state.opponent_bench), revealed_hand_size=game_state.opponent_hand_count,
        revealed_prizes_remaining=game_state.opponent_prizes, revealed_discard=game_state.opponent_discard,
        game_phase="early" if orchestrator.current_turn < 5 else "mid"))

    arch = orchestrator.opponent_model.identified_archetype
    if arch != "unknown" and arch in orchestrator.opponent_model.archetypes:
        pool = orchestrator.opponent_model.archetypes[arch].get("card_pool", [])
        sig = orchestrator.opponent_model.archetypes[arch].get("signature_cards", [])
        new_deck_dict = {}
        for cid in sig:
            try: new_deck_dict[int(cid)] = 4
            except (ValueError, TypeError): pass
        for cid in pool:
            try:
                cid_int = int(cid)
                if cid_int not in new_deck_dict: new_deck_dict[cid_int] = 2
            except (ValueError, TypeError): pass
        if new_deck_dict:
            orchestrator.belief_tracker.assumed_deck = new_deck_dict
    elif not orchestrator.belief_tracker.assumed_deck:
        # BUG 16: Before archetype is identified, seed with a generic prior
        # based on revealed opponent cards so far
        generic_deck = {}
        for cid in getattr(orchestrator.opponent_model, 'revealed_state', []):
            try:
                cid_int = int(cid) if not isinstance(cid, int) else cid
                generic_deck[cid_int] = generic_deck.get(cid_int, 0) + 1
            except (ValueError, TypeError):
                pass
        # Add common Trainer counts seen in most decks
        for basic_trainer_id in [1121, 1102, 1086, 1213]:  # Ultra Ball, Dusk Ball, Poffin, Judge
            if basic_trainer_id not in generic_deck:
                generic_deck[basic_trainer_id] = 2
        if generic_deck:
            orchestrator.belief_tracker.assumed_deck = generic_deck

def check_lethal_helper(game_state, boss_prob: float = 0.0):
    my_active = game_state.my_active_pokemon or {}
    my_attached = len(my_active.get("attached", []) or my_active.get("energies", [])) if isinstance(my_active, dict) else 0

    from cb_agents.card_registry import CardRegistry
    registry = CardRegistry()
    max_damage = 0
    
    my_active_id = None
    if isinstance(my_active, dict):
        my_active_id = my_active.get("id")
    else:
        my_active_id = my_active
        
    if my_active_id is not None and getattr(game_state, "legal_attacks", []):
        try:
            card = registry.get_full_skill(my_active_id)
            if card:
                max_damage = card.damage_output
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"Lethal helper active skill lookup failed: {e}")
    
    active = game_state.opponent_active
    opp_active_id = None
    if active:
        try:
            opp_active_id = int(active.get("id") if isinstance(active, dict) else active)
        except Exception as e:
            import logging
            logging.getLogger(__name__).debug(f"Lethal helper opponent active ID parse failed: {e}")
        
    lethal_result = pipeline.check_lethal(
        my_damage=max_damage, opp_hp=game_state.opponent_active_hp,
        legal_attacks=game_state.legal_attacks, opp_active_id=opp_active_id,
        my_hp=game_state.my_active_hp, legal_retreats=game_state.legal_retreats,
        my_attached=my_attached, boss_prob=boss_prob)
    return lethal_result

def handle_time_manager_helper(orchestrator, time_elapsed, legal_actions_list, game_state):
    from router.bus import TimePacket
    from cb_agents.heuristic_pipeline import pipeline

    def _get_f(obj, k, default=None):
        if isinstance(obj, dict): return obj.get(k, default)
        return getattr(obj, k, default)

    time_result = orchestrator.bus.dispatch('TimeManager', TimePacket(
        time_elapsed=time_elapsed, time_limit=600.0, legal_actions=legal_actions_list).__dict__)

    t_dir = _get_f(time_result, 'directive')
    t_act = _get_f(time_result, 'action_override')

    if t_dir == 'FORCE_PASS':
        if 'pass' in legal_actions_list:
            return 'pass'
        elif legal_actions_list:
            return legal_actions_list[0]
        else:
            return 'pass'
    if t_act is not None: return t_act
    if t_dir == 'FAST_MOVE':
        gs_dict = game_state.__dict__ if not isinstance(game_state, dict) else game_state
        best_action, best_score = 'pass', -float('inf')
        for a in legal_actions_list:
            s = pipeline.score_action(a, gs_dict)
            if s > best_score:
                best_score, best_action = s, a
        return best_action
    return None