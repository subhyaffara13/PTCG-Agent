
def _interp_limit(
    invalid: npt.NDArray[np.bool_], fw_limit: int | None, bw_limit: int | None
) -> np.ndarray:
    """
    Get indexers of values that won't be filled
    because they exceed the limits.

    Parameters
    ----------
    invalid : np.ndarray[bool]
    fw_limit : int or None
        forward limit to index
    bw_limit : int or None
        backward limit to index

    Returns
    -------
    set of indexers

    Notes
    -----
    This is equivalent to the more readable, but slower

    .. code-block:: python

        def _interp_limit(invalid, fw_limit, bw_limit):
            for x in np.where(invalid)[0]:
                if invalid[max(0, x - fw_limit) : x + bw_limit + 1].all():
                    yield x
    """
    # handle forward first; the backward direction is the same except
    # 1. operate on the reversed array
    # 2. subtract the returned indices from N - 1
    N = len(invalid)
    f_idx = np.array([], dtype=np.int64)
    b_idx = np.array([], dtype=np.int64)
    assume_unique = True

    def inner(invalid, limit: int):
        limit = min(limit, N - 1)
        windowed = np.lib.stride_tricks.sliding_window_view(invalid, limit + 1).all(1)
        idx = np.union1d(
            np.where(windowed)[0] + limit,
            np.where((~invalid[: limit + 1]).cumsum() == 0)[0],
        )
        return idx

    if fw_limit is not None:
        if fw_limit == 0:
            f_idx = np.where(invalid)[0]
            assume_unique = False
        else:
            f_idx = inner(invalid, fw_limit)

    if bw_limit is not None:
        if bw_limit == 0:
            # then we don't even need to care about backwards
            # just use forwards
            return f_idx
        else:
            b_idx = N - 1 - inner(invalid[::-1], bw_limit)
            if fw_limit == 0:
                return b_idx

    return np.intersect1d(f_idx, b_idx, assume_unique=assume_unique)

