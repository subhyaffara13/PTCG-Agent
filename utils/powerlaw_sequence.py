
def powerlaw_sequence(n, exponent=2.0, seed=None):
    """
    Return sample sequence of length n from a power law distribution.
    """
    return [seed.paretovariate(exponent - 1) for i in range(n)]

