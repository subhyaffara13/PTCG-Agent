
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

