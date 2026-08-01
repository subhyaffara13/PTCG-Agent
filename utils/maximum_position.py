
def maximum_position(input, labels=None, index=None):
    """
    Find the positions of the maximums of the values of an array at labels.

    For each region specified by `labels`, the position of the maximum
    value of `input` within the region is returned.

    Parameters
    ----------
    input : array_like
        Array_like of values.
    labels : array_like, optional
        An array of integers marking different regions over which the
        position of the maximum value of `input` is to be computed.
        `labels` must have the same shape as `input`. If `labels` is not
        specified, the location of the first maximum over the whole
        array is returned.

        The `labels` argument only works when `index` is specified.
    index : array_like, optional
        A list of region labels that are taken into account for finding the
        location of the maxima. If `index` is None, the first maximum
        over all elements where `labels` is non-zero is returned.

        The `index` argument only works when `labels` is specified.

    Returns
    -------
    output : list of tuples of ints
        List of tuples of ints that specify the location of maxima of
        `input` over the regions determined by `labels` and whose index
        is in `index`.

        If `index` or `labels` are not specified, a tuple of ints is
        returned specifying the location of the ``first`` maximal value
        of `input`.

    See Also
    --------
    label, minimum, median, maximum_position, extrema, sum, mean, variance,
    standard_deviation

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.array([[1, 2, 0, 0],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])
    >>> ndimage.maximum_position(a)
    (3, 0)

    Features to process can be specified using `labels` and `index`:

    >>> lbl = np.array([[0, 1, 2, 3],
    ...                 [0, 1, 2, 3],
    ...                 [0, 1, 2, 3],
    ...                 [0, 1, 2, 3]])
    >>> ndimage.maximum_position(a, lbl, 1)
    (1, 1)

    If no index is given, non-zero `labels` are processed:

    >>> ndimage.maximum_position(a, lbl)
    (2, 3)

    If there are no maxima, the position of the first element is returned:

    >>> ndimage.maximum_position(a, lbl, 2)
    (0, 2)

    """
    dims = np.array(np.asarray(input).shape)
    # see np.unravel_index to understand this line.
    dim_prod = np.cumprod([1] + list(dims[:0:-1]))[::-1]

    result = _select(input, labels, index, find_max_positions=True)[0]

    if np.isscalar(result):
        return tuple((result // dim_prod) % dims)

    return [tuple(v) for v in (result.reshape(-1, 1) // dim_prod) % dims]

