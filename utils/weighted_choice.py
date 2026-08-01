
def weighted_choice(mapping, seed=None):
    """Returns a single element from a weighted sample.

    The input is a dictionary of items with weights as values.
    """
    # use roulette method
    rnd = seed.random() * sum(mapping.values())
    for k, w in mapping.items():
        rnd -= w
        if rnd < 0:
            return k

