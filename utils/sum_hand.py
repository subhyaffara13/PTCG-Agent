
def sum_hand(hand):
    """Returns the total points in a hand."""
    return sum(hand) + (10 * usable_ace(hand))


def sum_hand(hand):  # Return current hand total
    if usable_ace(hand):
        return sum(hand) + 10
    return sum(hand)


def sum_hand(hand):  # Return current hand total
    if usable_ace(hand):
        return sum(hand) + 10
    return sum(hand)

