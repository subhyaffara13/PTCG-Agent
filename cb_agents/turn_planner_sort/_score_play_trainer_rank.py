from . import _dead_weight_heuristic, _registry

def _score_play_trainer_rank(action, game_state):
    micro = 0
    name = action.split(":", 1)[1]
    has_dead = _dead_weight_heuristic([action], game_state)
    _discard_search = {"ultra ball", "earthen vessel"}
    if has_dead and any(ds in name.lower() for ds in _discard_search):
        micro -= 6
    elif any(k in name for k in {"Research", "Professor", "Iono", "Carmine", "Lillie", "Colress"}):
        dc = game_state.get("my_deck_count", 60)
        opp_dc = game_state.get("opponent_deck_count", 60)
        if dc <= 3:
            micro += 200
        elif dc <= 5 and not any(k in name for k in {"Iono", "Judge"}):
            micro += 100
        elif dc <= 7 and not any(k in name for k in {"Iono", "Judge"}):
            micro += 25
        elif dc <= 20 and dc < opp_dc - 3 and not any(k in name for k in {"Iono", "Judge"}):
            micro += 12
        else:
            micro -= 5
    is_iono_judge = any(k in name for k in {"Iono", "Judge"})
    if is_iono_judge:
        dc = game_state.get("my_deck_count", 60)
        opp_dc = game_state.get("opponent_deck_count", 60)
        opp_searched = game_state.get("opponent_searched_last_turn", False)
        opp_passed_empty = game_state.get("opponent_passed_empty_last_turn", False)
        opp_prizes = game_state.get("opponent_prizes", 6)
        opp_hand_count = game_state.get("opponent_hand_count", 0)
        if opp_prizes <= 2 and opp_hand_count >= 4:
            micro -= 30
        elif opp_searched:
            micro -= 15
        elif opp_passed_empty:
            micro += 25
        elif opp_dc < dc and opp_dc < 12:
            micro -= 15
        elif opp_dc < 8:
            micro += 50
            micro -= 10
    elif "Ball" in name:
        micro -= 1
    return micro
