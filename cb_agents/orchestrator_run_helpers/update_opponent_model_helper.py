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

