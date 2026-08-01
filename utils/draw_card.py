
def draw_card(key, hand, index):
    """Draws a new card and adds it to a hand."""
    new_card, key = random_card(key)
    hand = hand.at[index].set(new_card)
    return key, hand, index + 1


def draw_card(np_random):
    return int(np_random.choice(deck))


def draw_card(np_random):
    return int(np_random.choice(deck))

