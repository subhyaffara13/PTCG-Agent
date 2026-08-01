
def _process_prize_tracker(game_state: dict, prize_tracker: PrizeTracker, packet) -> dict:
    initial_decklist = game_state.get("my_decklist", {})
    if initial_decklist and not prize_tracker.initial_decklist:
        prize_tracker.record_initial_decklist(initial_decklist)
    hand_ids = game_state.get("my_hand", [])
    if isinstance(hand_ids, list) and hand_ids and prize_tracker.initial_decklist:
        is_search = game_state.get("is_searching", False) or (isinstance(game_state.get("my_deck", []), list) and len(game_state.get("my_deck", [])) > 0)
        if is_search:
            discard_ids = game_state.get("my_discard", [])
            board_ids = list(game_state.get("my_board", []))
            active = game_state.get("my_active_pokemon", {})
            if isinstance(active, dict):
                aid = active.get("id")
                if aid is not None:
                    board_ids.append(int(aid) if not isinstance(aid, int) else aid)
                for att in active.get("attached", []):
                    try: board_ids.append(int(att))
                    except Exception as e:
                        logger.debug(f"Attached active card ID parse failed: {e}")
            for poke in game_state.get("my_bench", []):
                if isinstance(poke, dict):
                    pid = poke.get("id")
                    if pid is not None:
                        board_ids.append(int(pid) if not isinstance(pid, int) else pid)
                    for att in poke.get("attached", []):
                        try: board_ids.append(int(att))
                        except Exception as e:
                            logger.debug(f"Attached bench card ID parse failed: {e}")
            deck_contents = game_state.get("my_deck", [])
            deck_remaining = game_state.get("my_deck_count", 0)
            prize_tracker.on_deck_search(hand_ids, discard_ids, board_ids, deck_contents, deck_remaining)
    prized_enrich = prize_tracker.get_certainty_enrichment()
    if prized_enrich:
        game_state.update(prized_enrich)
        prized_card_types = len(prized_enrich.get('prized_card_ids', {}))
        logger.debug(f"Injected prized certainty into game_state: {prized_card_types} card types")
    return game_state


def _process_prize_tracker(game_state: dict, prize_tracker: PrizeTracker, packet) -> dict:
    initial_decklist = game_state.get("my_decklist", {})
    if initial_decklist and not prize_tracker.initial_decklist:
        prize_tracker.record_initial_decklist(initial_decklist)
    hand_ids = game_state.get("my_hand", [])
    if isinstance(hand_ids, list) and hand_ids and prize_tracker.initial_decklist:
        is_search = game_state.get("is_searching", False) or (isinstance(game_state.get("my_deck", []), list) and len(game_state.get("my_deck", [])) > 0)
        if is_search:
            discard_ids = game_state.get("my_discard", [])
            board_ids = list(game_state.get("my_board", []))
            active = game_state.get("my_active_pokemon", {})
            if isinstance(active, dict):
                aid = active.get("id")
                if aid is not None:
                    board_ids.append(int(aid) if not isinstance(aid, int) else aid)
                for att in active.get("attached", []):
                    try: board_ids.append(int(att))
                    except Exception as e:
                        logger.debug(f"Attached active card ID parse failed: {e}")
            for poke in game_state.get("my_bench", []):
                if isinstance(poke, dict):
                    pid = poke.get("id")
                    if pid is not None:
                        board_ids.append(int(pid) if not isinstance(pid, int) else pid)
                    for att in poke.get("attached", []):
                        try: board_ids.append(int(att))
                        except Exception as e:
                            logger.debug(f"Attached bench card ID parse failed: {e}")
            deck_contents = game_state.get("my_deck", [])
            deck_remaining = game_state.get("my_deck_count", 0)
            prize_tracker.on_deck_search(hand_ids, discard_ids, board_ids, deck_contents, deck_remaining)
    prized_enrich = prize_tracker.get_certainty_enrichment()
    if prized_enrich:
        game_state.update(prized_enrich)
        prized_card_types = len(prized_enrich.get('prized_card_ids', {}))
        logger.debug(f"Injected prized certainty into game_state: {prized_card_types} card types")
    return game_state


def _process_prize_tracker(game_state: dict, prize_tracker: PrizeTracker, packet) -> dict:
    initial_decklist = game_state.get("my_decklist", {})
    if initial_decklist and not prize_tracker.initial_decklist:
        prize_tracker.record_initial_decklist(initial_decklist)
    hand_ids = game_state.get("my_hand", [])
    if isinstance(hand_ids, list) and hand_ids and prize_tracker.initial_decklist:
        is_search = game_state.get("is_searching", False) or (isinstance(game_state.get("my_deck", []), list) and len(game_state.get("my_deck", [])) > 0)
        if is_search:
            discard_ids = game_state.get("my_discard", [])
            board_ids = list(game_state.get("my_board", []))
            active = game_state.get("my_active_pokemon", {})
            if isinstance(active, dict):
                aid = active.get("id")
                if aid is not None:
                    board_ids.append(int(aid) if not isinstance(aid, int) else aid)
                for att in active.get("attached", []):
                    try: board_ids.append(int(att))
                    except Exception as e:
                        logger.debug(f"Attached active card ID parse failed: {e}")
            for poke in game_state.get("my_bench", []):
                if isinstance(poke, dict):
                    pid = poke.get("id")
                    if pid is not None:
                        board_ids.append(int(pid) if not isinstance(pid, int) else pid)
                    for att in poke.get("attached", []):
                        try: board_ids.append(int(att))
                        except Exception as e:
                            logger.debug(f"Attached bench card ID parse failed: {e}")
            deck_contents = game_state.get("my_deck", [])
            deck_remaining = game_state.get("my_deck_count", 0)
            prize_tracker.on_deck_search(hand_ids, discard_ids, board_ids, deck_contents, deck_remaining)
    prized_enrich = prize_tracker.get_certainty_enrichment()
    if prized_enrich:
        game_state.update(prized_enrich)
        prized_card_types = len(prized_enrich.get('prized_card_ids', {}))
        logger.debug(f"Injected prized certainty into game_state: {prized_card_types} card types")
    return game_state


def _process_prize_tracker(game_state: dict, prize_tracker: PrizeTracker, packet) -> dict:
    initial_decklist = game_state.get("my_decklist", {})
    if initial_decklist and not prize_tracker.initial_decklist:
        prize_tracker.record_initial_decklist(initial_decklist)
    hand_ids = game_state.get("my_hand", [])
    if isinstance(hand_ids, list) and hand_ids and prize_tracker.initial_decklist:
        is_search = game_state.get("is_searching", False) or (isinstance(game_state.get("my_deck", []), list) and len(game_state.get("my_deck", [])) > 0)
        if is_search:
            discard_ids = game_state.get("my_discard", [])
            board_ids = list(game_state.get("my_board", []))
            active = game_state.get("my_active_pokemon", {})
            if isinstance(active, dict):
                aid = active.get("id")
                if aid is not None:
                    board_ids.append(int(aid) if not isinstance(aid, int) else aid)
                for att in active.get("attached", []):
                    try: board_ids.append(int(att))
                    except Exception as e:
                        logger.debug(f"Attached active card ID parse failed: {e}")
            for poke in game_state.get("my_bench", []):
                if isinstance(poke, dict):
                    pid = poke.get("id")
                    if pid is not None:
                        board_ids.append(int(pid) if not isinstance(pid, int) else pid)
                    for att in poke.get("attached", []):
                        try: board_ids.append(int(att))
                        except Exception as e:
                            logger.debug(f"Attached bench card ID parse failed: {e}")
            deck_contents = game_state.get("my_deck", [])
            deck_remaining = game_state.get("my_deck_count", 0)
            prize_tracker.on_deck_search(hand_ids, discard_ids, board_ids, deck_contents, deck_remaining)
    prized_enrich = prize_tracker.get_certainty_enrichment()
    if prized_enrich:
        game_state.update(prized_enrich)
        prized_card_types = len(prized_enrich.get('prized_card_ids', {}))
        logger.debug(f"Injected prized certainty into game_state: {prized_card_types} card types")
    return game_state


def _process_prize_tracker(game_state: dict, prize_tracker: PrizeTracker, packet) -> dict:
    initial_decklist = game_state.get("my_decklist", {})
    if initial_decklist and not prize_tracker.initial_decklist:
        prize_tracker.record_initial_decklist(initial_decklist)
    hand_ids = game_state.get("my_hand", [])
    if isinstance(hand_ids, list) and hand_ids and prize_tracker.initial_decklist:
        is_search = game_state.get("is_searching", False) or (isinstance(game_state.get("my_deck", []), list) and len(game_state.get("my_deck", [])) > 0)
        if is_search:
            discard_ids = game_state.get("my_discard", [])
            board_ids = list(game_state.get("my_board", []))
            active = game_state.get("my_active_pokemon", {})
            if isinstance(active, dict):
                aid = active.get("id")
                if aid is not None:
                    board_ids.append(int(aid) if not isinstance(aid, int) else aid)
                for att in active.get("attached", []):
                    try: board_ids.append(int(att))
                    except: pass
            for poke in game_state.get("my_bench", []):
                if isinstance(poke, dict):
                    pid = poke.get("id")
                    if pid is not None:
                        board_ids.append(int(pid) if not isinstance(pid, int) else pid)
                    for att in poke.get("attached", []):
                        try: board_ids.append(int(att))
                        except: pass
            deck_contents = game_state.get("my_deck", [])
            deck_remaining = game_state.get("my_deck_count", 0)
            prize_tracker.on_deck_search(hand_ids, discard_ids, board_ids, deck_contents, deck_remaining)
    prized_enrich = prize_tracker.get_certainty_enrichment()
    if prized_enrich:
        game_state.update(prized_enrich)
        prized_card_types = len(prized_enrich.get('prized_card_ids', {}))
        logger.debug(f"Injected prized certainty into game_state: {prized_card_types} card types")
    return game_state

