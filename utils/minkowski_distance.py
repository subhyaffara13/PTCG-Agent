import os

def minkowski_distance(x, y, p=2.0):
    """Compute the L**p distance between two arrays.

    The last dimensions of `x` and `y` must be the same length.  Any
    other dimensions must be compatible for broadcasting.

    .. deprecated:: 1.18.0
        This function is deprecated in favor of `scipy.spatial.distance.minkowski`
        and will be removed in SciPy 1.20.0.

    Parameters
    ----------
    x : (..., K) array_like
        Input array.
    y : (..., K) array_like
        Input array.
    p : float, 1 <= p <= infinity
        Which Minkowski p-norm to use.

    Returns
    -------
    dist : ndarray
        Distance between the input arrays.

    Examples
    --------
    >>> from scipy.spatial import minkowski_distance
    >>> minkowski_distance([[0, 0], [0, 0]], [[1, 1], [0, 1]])
    array([ 1.41421356,  1.        ])

    """
    msg = ("`minkowski_distance` is deprecated in favor of "
           "`scipy.spatial.distance.minkowski` as of SciPy 1.18.0 and will be removed "
           "in SciPy 1.20.0.")
    warnings.warn(msg, DeprecationWarning,
                  skip_file_prefixes=(os.path.dirname(__file__),))
    x = np.asarray(x)
    y = np.asarray(y)
    if p == np.inf or p == 1:
        return minkowski_distance_p(x, y, p)
    else:
        return minkowski_distance_p(x, y, p)**(1./p)

