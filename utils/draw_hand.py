
def draw_hand(key, hand):
    """Draws a starting hand of two random cards."""
    new_card, key = random_card(key)
    hand = hand.at[0].set(new_card)
    new_card, key = random_card(key)
    hand = hand.at[1].set(new_card)
    return hand, key


def draw_hand(np_random):
    return [draw_card(np_random), draw_card(np_random)]


def draw_hand(np_random):
    return [draw_card(np_random), draw_card(np_random)]

