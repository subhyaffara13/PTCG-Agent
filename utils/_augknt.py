
def _augknt(x, k):
    """Construct a knot vector appropriate for the order-k interpolation."""
    return np.r_[(x[0],)*k, x, (x[-1],)*k]

