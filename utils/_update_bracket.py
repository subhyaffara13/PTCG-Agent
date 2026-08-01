
def _update_bracket(ab, fab, c, fc):
    """Update a bracket given (c, fc), return the discarded endpoints."""
    fa, fb = fab
    idx = (0 if np.sign(fa) * np.sign(fc) > 0 else 1)
    rx, rfx = ab[idx], fab[idx]
    fab[idx] = fc
    ab[idx] = c
    return rx, rfx

