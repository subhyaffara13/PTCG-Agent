
def _get_even_parity_terms(n):
    """
    Returns a list of lists, with all possible combinations of n zeros and ones
    with an even number of ones.
    """
    return [e for e in [ibin(i, n) for i in range(2**n)] if sum(e) % 2 == 0]

