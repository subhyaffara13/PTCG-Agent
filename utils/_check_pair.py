
def _check_pair(minterm1, minterm2):
    """
    Checks if a pair of minterms differs by only one bit. If yes, returns
    index, else returns `-1`.
    """
    # Early termination seems to be faster than list comprehension,
    # at least for large examples.
    index = -1
    for x, i in enumerate(minterm1):  # zip(minterm1, minterm2) is slower
        if i != minterm2[x]:
            if index == -1:
                index = x
            else:
                return -1
    return index

