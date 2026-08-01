
def moderatef(f):
    """
    This function moderates the function value of a MINIMIZATION problem. It replaces
    NaN and any value above FUNCMAX by FUNCMAX.
    """
    f = FUNCMAX if np.isnan(f) else f
    f = np.clip(f, -REALMAX, FUNCMAX)
    # We may moderate huge negative function values as follows, but we decide not to.
    # f = np.clip(f, -FUNCMAX, FUNCMAX)
    return f

