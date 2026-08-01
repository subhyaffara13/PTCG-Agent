
def getitem_returns_view(arr, key) -> bool:
    """
    Check if an ``arr.__getitem__`` call with given ``key`` would return a view
    or not.
    """
    if not isinstance(key, tuple):
        key = (key,)

    # filter out Ellipsis and np.newaxis
    key = tuple(k for k in key if k is not Ellipsis and k is not np.newaxis)
    if not key:
        return True
    # single integer gives view if selecting subset of 2D array
    if arr.ndim == 2 and lib.is_integer(key[0]):
        return True
    # slices always give views
    if all(isinstance(k, slice) for k in key):
        return True
    return False

