
def _unscale(x, C, b_scale):
    """
    Converts solution to _autoscale problem -> solution to original problem.
    """

    try:
        n = len(C)
        # fails if sparse or scalar; that's OK.
        # this is only needed for original simplex (never sparse)
    except TypeError:
        n = len(x)

    return x[:n]*b_scale*C

