
def moderatec(c):
    """
    This function moderates the constraint value, the constraint demanding this value
    to be NONNEGATIVE. It replaces any value below -CONSTRMAX by -CONSTRMAX, and any
    NaN or value above CONSTRMAX by CONSTRMAX.
    """
    np.nan_to_num(c, copy=False, nan=CONSTRMAX)
    c = np.clip(c, -CONSTRMAX, CONSTRMAX)
    return c

