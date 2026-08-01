
def random_card(key):
    """Draws a randowm card (with replacement)."""
    key = random.split(key)[0]
    choice = random.choice(key, deck, shape=(1,))

    return choice[0].astype(int), key

