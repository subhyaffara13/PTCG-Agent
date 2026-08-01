
def get_precision(array: np.ndarray | Sequence[float]) -> int:
    to_begin = array[0] if array[0] > 0 else None
    to_end = 100 - array[-1] if array[-1] < 100 else None
    diff = np.ediff1d(array, to_begin=to_begin, to_end=to_end)
    diff = abs(diff)
    prec = -np.floor(np.log10(np.min(diff))).astype(int)
    prec = max(1, prec)
    return prec


def get_precision(dtype) -> SupportsFloat:
    """Get precision of a data type."""
    if np.issubdtype(dtype, np.floating):
        return np.finfo(dtype).precision
    else:
        return np.inf

