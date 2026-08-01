
def minimum_position(input, labels=None, index=None):
    """
    Find the positions of the minimums of the values of an array at labels.

    Parameters
    ----------
    input : array_like
        Array_like of values.
    labels : array_like, optional
        An array of integers marking different regions over which the
        position of the minimum value of `input` is to be computed.
        `labels` must have the same shape as `input`. If `labels` is not
        specified, the location of the first minimum over the whole
        array is returned.

        The `labels` argument only works when `index` is specified.
    index : array_like, optional
        A list of region labels that are taken into account for finding the
        location of the minima. If `index` is None, the ``first`` minimum
        over all elements where `labels` is non-zero is returned.

        The `index` argument only works when `labels` is specified.

    Returns
    -------
    output : list of tuples of ints
        Tuple of ints or list of tuples of ints that specify the location
        of minima of `input` over the regions determined by `labels` and
        whose index is in `index`.

        If `index` or `labels` are not specified, a tuple of ints is
        returned specifying the location of the first minimal value of `input`.

    See Also
    --------
    label, minimum, median, maximum_position, extrema, sum, mean, variance,
    standard_deviation

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[10, 20, 30],
    ...               [40, 80, 100],
    ...               [1, 100, 200]])
    >>> b = np.array([[1, 2, 0, 1],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])

    >>> from scipy import ndimage

    >>> ndimage.minimum_position(a)
    (2, 0)
    >>> ndimage.minimum_position(b)
    (0, 2)

    Features to process can be specified using `labels` and `index`:

    >>> label, pos = ndimage.label(a)
    >>> ndimage.minimum_position(a, label, index=np.arange(1, pos+1))
    [(2, 0)]

    >>> label, pos = ndimage.label(b)
    >>> ndimage.minimum_position(b, label, index=np.arange(1, pos+1))
    [(0, 0), (0, 3), (3, 1)]

    """
    dims = np.array(np.asarray(input).shape)
    # see np.unravel_index to understand this line.
    dim_prod = np.cumprod([1] + list(dims[:0:-1]))[::-1]

    result = _select(input, labels, index, find_min_positions=True)[0]

    if np.isscalar(result):
        return tuple((result // dim_prod) % dims)

    return [tuple(v) for v in (result.reshape(-1, 1) // dim_prod) % dims]

