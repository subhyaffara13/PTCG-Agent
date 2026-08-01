
def _maybe_repeat(arr: ArrayLike, index: Index | None) -> ArrayLike:
    """
    If we have a length-1 array and an index describing how long we expect
    the result to be, repeat the array.
    """
    if index is not None:
        if 1 == len(arr) != len(index):
            arr = arr.repeat(len(index))
    return arr

