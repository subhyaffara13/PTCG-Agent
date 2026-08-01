
def _asindices(idx, length, format):
    """Convert `idx` to a valid index for an axis with a given length.

    Subclasses that need special validation can override this method.
    """
    try:
        ix = np.asarray(idx)
    except (ValueError, TypeError, MemoryError) as e:
        raise IndexError('invalid index') from e

    if format != "coo" and ix.ndim not in (1, 2) or format == "coo" and ix.ndim == 0:
        raise IndexError(f'Index dimension must be 1 or 2. Got {ix.ndim}')

    # LIL routines handle bounds-checking for us, so don't do it here.
    if format == "lil":
        return ix

    if ix.size == 0:
        return ix

    # Check bounds
    max_indx = ix.max()
    if max_indx >= length:
        raise IndexError(f'index ({max_indx}) out of range')

    min_indx = ix.min()
    if min_indx < 0:
        if min_indx < -length:
            raise IndexError(f'index ({min_indx}) out of range')
        if ix is idx or not ix.flags.owndata:
            ix = ix.copy()
        ix[ix < 0] += length
    return ix

