
def _fr0(a):
    """fix rank-0 --> rank-1"""
    if a.ndim == 0:
        a = a.reshape((1,))
    return a

