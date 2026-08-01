
def optimal_leaf_ordering(Z, y, metric='euclidean'):
    """
    Given a linkage matrix Z and distance, reorder the cut tree.

    Parameters
    ----------
    Z : ndarray
        The hierarchical clustering encoded as a linkage matrix. See
        `linkage` for more information on the return structure and
        algorithm.
    y : ndarray
        The condensed distance matrix from which Z was generated.
        Alternatively, a collection of m observation vectors in n
        dimensions may be passed as an m by n array.
    metric : str or function, optional
        The distance metric to use in the case that y is a collection of
        observation vectors; ignored otherwise. See the ``pdist``
        function for a list of valid distance metrics. A custom distance
        function can also be used.

    Returns
    -------
    Z_ordered : ndarray
        A copy of the linkage matrix Z, reordered to minimize the distance
        between adjacent leaves.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.cluster import hierarchy
    >>> rng = np.random.default_rng()
    >>> X = rng.standard_normal((10, 10))
    >>> Z = hierarchy.ward(X)
    >>> hierarchy.leaves_list(Z)
    array([0, 3, 1, 9, 2, 5, 7, 4, 6, 8], dtype=int32)
    >>> hierarchy.leaves_list(hierarchy.optimal_leaf_ordering(Z, X))
    array([3, 0, 2, 5, 7, 4, 8, 6, 9, 1], dtype=int32)

    """
    xp = array_namespace(Z, y)
    Z = _asarray(Z, order='C', xp=xp)
    y = _asarray(y, order='C', dtype=xp.float64, xp=xp)
    lazy = is_lazy_array(Z)
    _is_valid_linkage(Z, throw=True, name='Z', xp=xp)

    if y.ndim == 1:
        distance.is_valid_y(y, throw=True, name='y')
    elif y.ndim == 2:
        if (not lazy and y.shape[0] == y.shape[1]
            and xp.all(xpx.isclose(xp.linalg.diagonal(y), 0))
            and xp.all(y >= 0) and xp.all(xpx.isclose(y, y.T))):
            warnings.warn('The symmetric non-negative hollow observation '
                          'matrix looks suspiciously like an uncondensed '
                          'distance matrix',
                          ClusterWarning, stacklevel=2)
        y = distance.pdist(y, metric)
    else:
        raise ValueError("`y` must be 1 or 2 dimensional.")
    if not lazy and not xp.all(xp.isfinite(y)):
        raise ValueError("The condensed distance matrix must contain only "
                         "finite values.")

    # The function name is prominently visible on the user-facing Dask dashboard;
    # make sure it is meaningful.
    def cy_optimal_leaf_ordering(Z, y, validate):
        if validate:
            _is_valid_linkage(Z, throw=True, name='Z', xp=np)
            if not np.all(np.isfinite(y)):
                raise ValueError("The condensed distance matrix must contain only "
                                 "finite values.")
        return _optimal_leaf_ordering.optimal_leaf_ordering(Z, y)

    return xpx.lazy_apply(cy_optimal_leaf_ordering, Z, y, validate=lazy,
                          shape=Z.shape, dtype=Z.dtype, as_numpy=True, xp=xp)

