
def is_natural(hand):
    """Returns if the hand is a natural blackjack."""
    return jnp.logical_and(
        jnp.logical_and(
            jnp.count_nonzero(hand) == 2, (jnp.count_nonzero(hand == 1) > 0)
        ),
        (jnp.count_nonzero(hand == 10) > 0),
    )


def is_natural(hand):  # Is this hand a natural blackjack?
    return sorted(hand) == [1, 10]


def is_natural(hand):  # Is this hand a natural blackjack?
    return sorted(hand) == [1, 10]

