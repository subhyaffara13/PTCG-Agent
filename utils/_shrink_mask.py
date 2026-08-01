
def _shrink_mask(m):
    """
    Shrink a mask to nomask if possible
    """
    if m.dtype.names is None and not m.any():
        return nomask
    else:
        return m

