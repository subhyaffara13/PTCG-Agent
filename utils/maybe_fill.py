
def maybe_fill(arr: np.ndarray) -> np.ndarray:
    """
    Fill numpy.ndarray with NaN, unless we have an integer or boolean dtype.
    """
    if arr.dtype.kind not in "iub":
        arr.fill(np.nan)
    return arr

