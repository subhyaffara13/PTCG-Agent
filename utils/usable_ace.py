
def usable_ace(hand):
    """Checks to se if a hand has a usable ace."""
    return jnp.logical_and((jnp.count_nonzero(hand == 1) > 0), (sum(hand) + 10 <= 21))


def usable_ace(hand):  # Does this hand have a usable ace?
    return int(1 in hand and sum(hand) + 10 <= 21)


def usable_ace(hand):  # Does this hand have a usable ace?
    return 1 in hand and sum(hand) + 10 <= 21

