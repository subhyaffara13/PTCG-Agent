
def score_state(gs: dict) -> float:
    if _HAS_CPP_SCORE and _ptcg_core is not None:
        try:
            return _ptcg_core.score_state(gs)
        except Exception as e:
            logger.debug(f"C++ score_state failed: {e}. Falling back to Python.")
    v = 0.0
    mp = gs.get("my_prizes", 6)
    opp_p = gs.get("opponent_prizes", 6)
    turn = gs.get("turn_number", 1)
    v += 0.15 * (opp_p - mp)
    v += 0.001 * (gs.get("my_active_hp", 100) - gs.get("opponent_active_hp", 100))
    
    # Reward state if we can KO opponent's active next turn
    ac = gs.get("my_active_pokemon") or {}
    opp_hp = gs.get("opponent_active_hp", 100)
    if isinstance(ac, dict):
        my_active_id = ac.get("id")
        if my_active_id is not None:
            try:
                card = _registry.get_full_skill(my_active_id)
                if card and card.damage_output >= opp_hp:
                    attached_count = len(ac.get("attached", []) or ac.get("energies", []))
                    if attached_count >= card.energy_cost:
                        v += 0.5  # Heavy state reward for having a lethal threat ready
            except Exception:
                pass

    # Turn-number awareness: early game favors setup, late game favors aggression
    if turn <= 3:
        v += 0.1  # Early game: slightly positive for having drawn well
    elif turn >= 10:
        v += 0.2 * (gs.get("my_bench_count", 0) >= 3)  # Late game: reward board presence

    target_bench = getattr(_registry, "target_bench_density", None)
    bench_size = len(gs.get("my_bench", [])) if isinstance(gs.get("my_bench"), list) else 0
    if target_bench and target_bench > 0:
        v += 0.15 * min(1.0, bench_size / target_bench)
    
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
    if opp_damage is None:
        opp_damage = 0
    my_hp = gs.get("my_active_hp")
    if my_hp is None:
        my_hp = 100
    if opp_damage > 0 and opp_damage >= my_hp:
        # Prize Baiting Check: if our active is a 1-prizer, opponent taking 1 prize sets up an aggressive Iono comeback!
        my_active_card_id = ac.get("id") if isinstance(ac, dict) else None
        is_one_prizer = True
        if my_active_card_id:
            try:
                card = _registry.get_full_skill(my_active_card_id)
                if card and any(t in card.card_name.lower() for t in (" ex", " v", "vstar", "vmax", "ex")):
                    is_one_prizer = False
            except Exception:
                pass
        
        has_iono = any("iono" in str(c).lower() for c in gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else False
        if is_one_prizer and has_iono and mp > 2:
            v += 0.2  # Prize Baiting: losing 1 prize sets up devastating Iono hand-lock next turn!
        else:
            v -= 0.8  # Standard lethal threat penalty
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


def score_state(gs: dict) -> float:
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
            except: pass
    v += 0.05 * ec
    return v


def score_state(gs: dict) -> float:
    if _HAS_CPP_SCORE and _ptcg_core is not None:
        try:
            return _ptcg_core.score_state(gs)
        except Exception as e:
            logger.debug(f"C++ score_state failed: {e}. Falling back to Python.")
    v = 0.0
    mp = gs.get("my_prizes", 6)
    opp_p = gs.get("opponent_prizes", 6)
    turn = gs.get("turn_number", 1)
    v += 0.15 * (opp_p - mp)
    v += 0.001 * (gs.get("my_active_hp", 100) - gs.get("opponent_active_hp", 100))
    
    # Reward state if we can KO opponent's active next turn
    ac = gs.get("my_active_pokemon") or {}
    opp_hp = gs.get("opponent_active_hp", 100)
    if isinstance(ac, dict):
        my_active_id = ac.get("id")
        if my_active_id is not None:
            try:
                card = _registry.get_full_skill(my_active_id)
                if card and card.damage_output >= opp_hp:
                    attached_count = len(ac.get("attached", []) or ac.get("energies", []))
                    if attached_count >= card.energy_cost:
                        v += 0.5  # Heavy state reward for having a lethal threat ready
            except Exception:
                pass

    # Turn-number awareness: early game favors setup, late game favors aggression
    if turn <= 3:
        v += 0.1  # Early game: slightly positive for having drawn well
    elif turn >= 10:
        v += 0.2 * (gs.get("my_bench_count", 0) >= 3)  # Late game: reward board presence

    target_bench = getattr(_registry, "target_bench_density", None)
    bench_size = len(gs.get("my_bench", [])) if isinstance(gs.get("my_bench"), list) else 0
    if target_bench and target_bench > 0:
        v += 0.15 * min(1.0, bench_size / target_bench)
    
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
    if opp_damage is None:
        opp_damage = 0
    my_hp = gs.get("my_active_hp")
    if my_hp is None:
        my_hp = 100
    if opp_damage > 0 and opp_damage >= my_hp:
        # Prize Baiting Check: if our active is a 1-prizer, opponent taking 1 prize sets up an aggressive Iono comeback!
        my_active_card_id = ac.get("id") if isinstance(ac, dict) else None
        is_one_prizer = True
        if my_active_card_id:
            try:
                card = _registry.get_full_skill(my_active_card_id)
                if card and any(t in card.card_name.lower() for t in (" ex", " v", "vstar", "vmax", "ex")):
                    is_one_prizer = False
            except Exception:
                pass
        
        has_iono = any("iono" in str(c).lower() for c in gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else False
        if is_one_prizer and has_iono and mp > 2:
            v += 0.2  # Prize Baiting: losing 1 prize sets up devastating Iono hand-lock next turn!
        else:
            v -= 0.8  # Standard lethal threat penalty
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

