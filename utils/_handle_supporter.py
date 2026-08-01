
def _handle_supporter(gs, hand, base_name, draw_cards):
    if any(k in base_name for k in {"research", "professor"}):
        gs["my_discard"] = gs.get("my_discard", []) + hand.copy()
        hand.clear()
        gs["my_hand"] = draw_cards(hand, gs, 7)
        return True
    if any(k in base_name for k in {"iono", "judge"}):
        gs["my_deck"] = gs.get("my_deck", []) + hand.copy()
        gs["my_deck_count"] = gs.get("my_deck_count", 60) + len(hand)
        hand.clear()
        gs["my_hand"] = draw_cards(hand, gs, 4)
        return True
    if any(k in base_name for k in {"larry", "skill"}) and "secret" not in base_name:
        target_count = 3
        current_hand = len(gs.get("my_hand", []))
        if current_hand < target_count:
            gs["my_hand"] = draw_cards(hand, gs, target_count - current_hand)
        return True
    return False


def _handle_supporter(gs, hand, base_name, draw_cards):
    if any(k in base_name for k in {"research", "professor"}):
        gs["my_discard"] = gs.get("my_discard", []) + hand.copy()
        hand.clear()
        gs["my_hand"] = draw_cards(hand, gs, 7)
        return True
    if any(k in base_name for k in {"iono", "judge"}):
        gs["my_deck"] = gs.get("my_deck", []) + hand.copy()
        gs["my_deck_count"] = gs.get("my_deck_count", 60) + len(hand)
        hand.clear()
        gs["my_hand"] = draw_cards(hand, gs, 4)
        return True
    if any(k in base_name for k in {"larry", "skill"}) and "secret" not in base_name:
        target_count = 3
        current_hand = len(gs.get("my_hand", []))
        if current_hand < target_count:
            gs["my_hand"] = draw_cards(hand, gs, target_count - current_hand)
        return True
    return False

