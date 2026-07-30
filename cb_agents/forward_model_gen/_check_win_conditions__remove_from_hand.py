from . import Any
from ._load_concede_thresholds__check_concede import _check_concede

def _check_win_conditions(gs: dict) -> None:
    if gs.get("my_prizes", 6) <= 0:
        gs["game_over"] = True
        gs["winner"] = "me"
        return
    if gs.get("opponent_prizes", 6) <= 0:
        gs["game_over"] = True
        gs["winner"] = "opponent"
        return
    if gs.get("deck_out_loss", False) or gs.get("my_deck_count", 60) < 0:
        gs["game_over"] = True
        gs["winner"] = "opponent"
        return
    if gs.get("opponent_deck_out", False) or gs.get("opponent_deck_count", 60) < 0:
        gs["game_over"] = True
        gs["winner"] = "me"
        return
    my_hp = gs.get("my_active_hp", 100) if gs.get("my_active_pokemon") else 0
    my_bench = gs.get("my_bench", [])
    if my_hp <= 0 and not my_bench:
        gs["game_over"] = True
        gs["winner"] = "opponent"
        return
    opp_hp = gs.get("opponent_active_hp", 100)
    opp_bench = gs.get("opponent_bench", [])
    if opp_hp <= 0 and not opp_bench:
        gs["game_over"] = True
        gs["winner"] = "me"
        return

    # Hopeless position check — concede to save simulation time
    if _check_concede(gs):
        gs["game_over"] = True
        gs["winner"] = "opponent"
        gs["conceded"] = True

def _remove_from_hand(hand: list, card_id: Any) -> None:
    try:
        hand.remove(card_id)
        return
    except (ValueError, TypeError):
        pass
    if isinstance(card_id, str):
        try:
            hand.remove(int(card_id))
            return
        except (ValueError, TypeError):
            pass

