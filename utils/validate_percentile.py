
def validate_percentile(q: float | Iterable[float]) -> np.ndarray:
    """
    Validate percentiles (used by describe and quantile).

    This function checks if the given float or iterable of floats is a valid percentile
    otherwise raises a ValueError.

    Parameters
    ----------
    q: float or iterable of floats
        A single percentile or an iterable of percentiles.

    Returns
    -------
    ndarray
        An ndarray of the percentiles if valid.

    Raises
    ------
    ValueError if percentiles are not in given interval([0, 1]).
    """
    q_arr = np.asarray(q)
    # Don't change this to an f-string. The string formatting
    # is too expensive for cases where we don't need it.
    msg = "percentiles should all be in the interval [0, 1]"
    if q_arr.ndim == 0:
        if not 0 <= q_arr <= 1:
            raise ValueError(msg)
    elif not all(0 <= qs <= 1 for qs in q_arr):
        raise ValueError(msg)
    return q_arr

