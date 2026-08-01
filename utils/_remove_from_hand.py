from typing import Any

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
