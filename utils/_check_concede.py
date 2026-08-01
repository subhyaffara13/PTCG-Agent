
def _check_concede(gs: dict) -> bool:
    prize_gap_min, deck_out_max, prevent_prize_gap = _load_concede_thresholds()
    my_prizes = gs.get("my_prizes", 6)
    opp_prizes = gs.get("opponent_prizes", 6)
    my_bench = gs.get("my_bench", [])
    my_hp = gs.get("my_active_hp", 100) if gs.get("my_active_pokemon") else 0
    my_deck = gs.get("my_deck_count", 60)

    # No Pokemon left on board
    if my_hp <= 0 and not my_bench:
        return True

    # Opponent has taken almost all prizes; we have taken none
    if my_prizes <= 0 and opp_prizes >= prize_gap_min:
        return True

    # Deck-out imminent with no realistic comeback (we need multiple KOs, opponent needs 0)
    if my_deck <= deck_out_max and opp_prizes >= prize_gap_min and my_prizes >= prevent_prize_gap:
        return True

    # Opponent about to take last prize and we can't prevent it
    if opp_prizes <= 1 and my_prizes >= prevent_prize_gap:
        opp_hp = gs.get("opponent_active_hp", 100)
        if opp_hp > 0:
            return True

    return False


def _check_concede(gs: dict) -> bool:
    prize_gap_min, deck_out_max, prevent_prize_gap = _load_concede_thresholds()
    my_prizes = gs.get("my_prizes", 6)
    opp_prizes = gs.get("opponent_prizes", 6)
    my_bench = gs.get("my_bench", [])
    my_hp = gs.get("my_active_hp", 100) if gs.get("my_active_pokemon") else 0
    my_deck = gs.get("my_deck_count", 60)

    # No Pokemon left on board
    if my_hp <= 0 and not my_bench:
        return True

    # Opponent has taken almost all prizes; we have taken none
    if my_prizes <= 0 and opp_prizes >= prize_gap_min:
        return True

    # Deck-out imminent with no realistic comeback (we need multiple KOs, opponent needs 0)
    if my_deck <= deck_out_max and opp_prizes >= prize_gap_min and my_prizes >= prevent_prize_gap:
        return True

    # Opponent about to take last prize and we can't prevent it
    if opp_prizes <= 1 and my_prizes >= prevent_prize_gap:
        opp_hp = gs.get("opponent_active_hp", 100)
        if opp_hp > 0:
            return True

    return False

