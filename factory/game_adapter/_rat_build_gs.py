def _build_game_state_from_observation(my_state, opp_state, current, select):
    from factory.game_adapter_state import build_game_state
    game_state = build_game_state(my_state, opp_state, current)
    options = select.get("option", [])
    game_state["legal_attacks"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (12, 13)]
    game_state["legal_attachments"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (8, 9)]
    sel_type = select.get("type"); sel_ctx = select.get("context")
    game_state["select_prize"] = bool(sel_ctx in ("prize", "select_prize") or sel_type == 2)
    game_state["select_type"] = sel_type; game_state["select_context"] = sel_ctx
    return game_state

def _parse_legal_options(options, my_state, game_state, registry):
    my_hand = game_state.get("my_hand", [])
    legal_bench, legal_evolutions = [], []
    for i, opt in enumerate(options):
        if opt.get("type") == 8:
            is_evo = False
            hand_idx = opt.get("index")
            if hand_idx is not None and 0 <= hand_idx < len(my_hand):
                card_id = my_hand[hand_idx]
                if registry and card_id:
                    try:
                        card = registry.get_full_skill(card_id)
                        if card:
                            from cb_agents.card_types import CardStage
                            if card.stage in (CardStage.STAGE1, CardStage.STAGE2) or card.previous_stage: is_evo = True
                    except Exception: pass
            if is_evo: legal_evolutions.append(str(i))
            else: legal_bench.append(str(i))
    game_state["legal_bench"] = legal_bench
    game_state["legal_evolutions"] = legal_evolutions
    game_state["legal_trainers"] = [str(i) for i, opt in enumerate(options) if opt.get("type") == 7]
    game_state["legal_retreats"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (10, 12)]
    game_state["legal_abilities"] = [str(i) for i, opt in enumerate(options) if opt.get("type") in (11, 15)]
    game_state["legal_prize_options"] = [str(i) for i, opt in enumerate(options) if opt.get("type") == 2]
