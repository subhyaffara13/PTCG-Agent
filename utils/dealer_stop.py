
def dealer_stop(val):
    """This function determines if the dealer should stop drawing."""
    return sum_hand(val[1]) < 17

