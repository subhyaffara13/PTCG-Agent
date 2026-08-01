
def extrema(input, labels=None, index=None):
    """
    Calculate the minimums and maximums of the values of an array
    at labels, along with their positions.

    Parameters
    ----------
    input : ndarray
        N-D image data to process.
    labels : ndarray, optional
        Labels of features in input.
        If not None, must be same shape as `input`.
    index : int or sequence of ints, optional
        Labels to include in output.  If None (default), all values where
        non-zero `labels` are used.

    Returns
    -------
    minimums, maximums : int or ndarray
        Values of minimums and maximums in each feature.
    min_positions, max_positions : tuple or list of tuples
        Each tuple gives the N-D coordinates of the corresponding minimum
        or maximum.

    See Also
    --------
    maximum, minimum, maximum_position, minimum_position, center_of_mass

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, 2, 0, 0],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])
    >>> from scipy import ndimage
    >>> ndimage.extrema(a)
    (0, 9, (0, 2), (3, 0))

    Features to process can be specified using `labels` and `index`:

    >>> lbl, nlbl = ndimage.label(a)
    >>> ndimage.extrema(a, lbl, index=np.arange(1, nlbl+1))
    (array([1, 4, 3]),
     array([5, 7, 9]),
     [(0, 0), (1, 3), (3, 1)],
     [(1, 0), (2, 3), (3, 0)])

    If no index is given, non-zero `labels` are processed:

    >>> ndimage.extrema(a, lbl)
    (1, 9, (0, 0), (3, 0))

    """
    dims = np.array(np.asarray(input).shape)
    # see np.unravel_index to understand this line.
    dim_prod = np.cumprod([1] + list(dims[:0:-1]))[::-1]

    minimums, min_positions, maximums, max_positions = _select(input, labels,
                                                               index,
                                                               find_min=True,
                                                               find_max=True,
                                                               find_min_positions=True,
                                                               find_max_positions=True)

    if np.isscalar(minimums):
        return (minimums, maximums, tuple((min_positions // dim_prod) % dims),
                tuple((max_positions // dim_prod) % dims))

    min_positions = [
        tuple(v) for v in (min_positions.reshape(-1, 1) // dim_prod) % dims
    ]
    max_positions = [
        tuple(v) for v in (max_positions.reshape(-1, 1) // dim_prod) % dims
    ]

    return minimums, maximums, min_positions, max_positions

