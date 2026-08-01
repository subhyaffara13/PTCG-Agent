
def _hand_strength(game_state: dict) -> str:
    hand = game_state.get("my_hand", [])
    hand_size = len(hand) if isinstance(hand, list) else 0
    if hand_size <= 2:
        return "weak"
    elif hand_size <= 4:
        return "medium"
    return "strong"


def _hand_strength(game_state: dict) -> str:
    hand = game_state.get("my_hand", [])
    hand_size = len(hand) if isinstance(hand, list) else 0
    if hand_size <= 2:
        return "weak"
    elif hand_size <= 4:
        return "medium"
    return "strong"


def _hand_strength(game_state: dict) -> str:
    hand = game_state.get("my_hand", [])
    hand_size = len(hand) if isinstance(hand, list) else 0
    if hand_size <= 2:
        return "weak"
    elif hand_size <= 4:
        return "medium"
    return "strong"

