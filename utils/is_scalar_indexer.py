
def is_scalar_indexer(indexer, ndim: int) -> bool:
    """
    Return True if we are all scalar indexers.

    Parameters
    ----------
    indexer : object
    ndim : int
        Number of dimensions in the object being indexed.

    Returns
    -------
    bool
    """
    if ndim == 1 and is_integer(indexer):
        # GH37748: allow indexer to be an integer for Series
        return True
    if isinstance(indexer, tuple) and len(indexer) == ndim:
        return all(is_integer(x) for x in indexer)
    return False

