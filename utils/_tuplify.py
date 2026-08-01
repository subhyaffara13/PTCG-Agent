
def _tuplify(ndim: int, loc: Hashable) -> tuple[Hashable | slice, ...]:
    """
    Given an indexer for the first dimension, create an equivalent tuple
    for indexing over all dimensions.

    Parameters
    ----------
    ndim : int
    loc : object

    Returns
    -------
    tuple
    """
    _tup: list[Hashable | slice]
    _tup = [slice(None, None) for _ in range(ndim)]
    _tup[0] = loc
    return tuple(_tup)

