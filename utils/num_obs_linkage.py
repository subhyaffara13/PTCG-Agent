
def num_obs_linkage(Z):
    """
    Return the number of original observations of the linkage matrix passed.

    Parameters
    ----------
    Z : ndarray
        The linkage matrix on which to perform the operation.

    Returns
    -------
    n : int
        The number of original observations in the linkage.

    Examples
    --------
    >>> from scipy.cluster.hierarchy import ward, num_obs_linkage
    >>> from scipy.spatial.distance import pdist

    >>> X = [[0, 0], [0, 1], [1, 0],
    ...      [0, 4], [0, 3], [1, 4],
    ...      [4, 0], [3, 0], [4, 1],
    ...      [4, 4], [3, 4], [4, 3]]

    >>> Z = ward(pdist(X))

    ``Z`` is a linkage matrix obtained after using the Ward clustering method
    with ``X``, a dataset with 12 data points.

    >>> num_obs_linkage(Z)
    12

    """
    xp = array_namespace(Z)
    Z = _asarray(Z, xp=xp)
    _is_valid_linkage(Z, throw=True, name='Z', xp=xp)
    return Z.shape[0] + 1

