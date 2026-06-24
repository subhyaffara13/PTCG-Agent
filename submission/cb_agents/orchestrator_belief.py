def sync_belief_tracker(belief_tracker, game_state: dict):
    """Synchronizes the belief tracker state with the current public game state."""
    belief_tracker.state.hand_size = game_state.get("opponent_hand_count", 5)
    belief_tracker.state.prize_size = game_state.get("opponent_prizes", 6)
    
    known_in_play = {}
    active = game_state.get("opponent_active")
    if active:
        active_id = active.get("id") if isinstance(active, dict) else active
        if active_id:
            try:
                known_in_play[int(active_id)] = 1
            except ValueError:
                pass
                
    for bench_item in game_state.get("opponent_bench", []):
        bench_id = bench_item.get("id") if isinstance(bench_item, dict) else bench_item
        if bench_id:
            try:
                bench_id_int = int(bench_id)
                known_in_play[bench_id_int] = known_in_play.get(bench_id_int, 0) + 1
            except ValueError:
                pass
                
    belief_tracker.state.known_in_play = known_in_play
    
    known_in_discard = {}
    for card_id in game_state.get("opponent_discard", []):
        try:
            card_id_int = int(card_id)
            known_in_discard[card_id_int] = known_in_discard.get(card_id_int, 0) + 1
        except ValueError:
            pass
    belief_tracker.state.known_in_discard = known_in_discard
    
    total_cards = sum(belief_tracker.assumed_deck.values()) if belief_tracker.assumed_deck else 60
    known_non_deck = (belief_tracker.state.hand_size + 
                      belief_tracker.state.prize_size + 
                      sum(known_in_play.values()) + 
                      sum(known_in_discard.values()))
    belief_tracker.state.deck_size = max(0, total_cards - known_non_deck)
    belief_tracker._recalculate_probabilities()
