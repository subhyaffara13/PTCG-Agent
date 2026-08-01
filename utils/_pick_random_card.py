
def _pick_random_card(gs):
    import random
    if gs.get("my_deck"):
        return random.choice(gs["my_deck"])
    if gs.get("my_decklist"):
        return random.choice(list(gs["my_decklist"].keys()))
    return 1


def _pick_random_card(gs):
    import random
    if gs.get("my_deck"):
        return random.choice(gs["my_deck"])
    if gs.get("my_decklist"):
        return random.choice(list(gs["my_decklist"].keys()))
    return 1

