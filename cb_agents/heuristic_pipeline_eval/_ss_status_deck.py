def _ss_status_deck(v, gs):
    my_status = gs.get("my_active_status", "")
    if my_status in ("poisoned", "burned"): v -= 0.15
    elif my_status in ("paralyzed", "asleep"): v -= 0.3
    opp_status = gs.get("opponent_active_status", "")
    if opp_status in ("paralyzed", "asleep"): v += 0.3
    elif opp_status in ("poisoned", "burned"): v += 0.15
    my_dc = gs.get("my_deck_count", 60); opp_dc = gs.get("opponent_deck_count", 60)
    if my_dc <= 3: v -= 0.5
    elif my_dc <= 8: v -= 0.2
    if opp_dc <= 3: v += 0.3
    elif opp_dc <= 8: v += 0.1
    if my_dc > 0 and opp_dc > 0:
        avg_draw = 1.5; my_turns = my_dc / avg_draw; opp_turns = opp_dc / avg_draw
        turns_diff = my_turns - opp_turns
        if turns_diff > 3: v += 0.4 + 0.05 * min(turns_diff, 8)
        elif turns_diff > 1: v += 0.15
        elif turns_diff < -3: v -= 0.4
        elif turns_diff < -1: v -= 0.15
    if my_dc > 0:
        hand_size = len(gs.get("my_hand", [])) if isinstance(gs.get("my_hand"), list) else 0
        turns_left = max(0, my_dc / 1.5)
        if turns_left <= 1: v -= 0.8
        elif turns_left <= 2: v -= 0.4
        elif turns_left <= 3: v -= 0.15
    return v
