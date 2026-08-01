
def distance_matrix(x, y, p=2.0, threshold=1000000):
    """Compute the distance matrix.

    Returns the matrix of all pair-wise distances.

    .. deprecated:: 1.18.0
        This function is deprecated in favor of `scipy.spatial.distance.cdist`
        and will be removed in SciPy 1.20.0.

    Parameters
    ----------
    x : (M, K) array_like
        Matrix of M vectors in K dimensions.
    y : (N, K) array_like
        Matrix of N vectors in K dimensions.
    p : float, 1 <= p <= infinity
        Which Minkowski p-norm to use.
    threshold : positive int
        If ``M * N * K`` > `threshold`, algorithm uses a Python loop instead
        of large temporary arrays.

    Returns
    -------
    result : (M, N) ndarray
        Matrix containing the distance from every vector in `x` to every vector
        in `y`.

    Examples
    --------
    >>> from scipy.spatial import distance_matrix
    >>> distance_matrix([[0,0],[0,1]], [[1,0],[1,1]])
    array([[ 1.        ,  1.41421356],
           [ 1.41421356,  1.        ]])

    """
    msg = ("`distance_matrix` is deprecated in favor of "
           "`scipy.spatial.distance.cdist` as of SciPy 1.18.0 and will be removed "
           "in SciPy 1.20.0.")
    warnings.warn(msg, DeprecationWarning,
                  skip_file_prefixes=(os.path.dirname(__file__),))
    x = np.asarray(x)
    m, k = x.shape
    y = np.asarray(y)
    n, kk = y.shape

    if k != kk:
        raise ValueError(f"x contains {k}-dimensional vectors but y contains "
                         f"{kk}-dimensional vectors")

    if m*n*k <= threshold:
        return minkowski_distance(x[:,np.newaxis,:],y[np.newaxis,:,:],p)
    else:
        result = np.empty((m,n),dtype=float)  # FIXME: figure out the best dtype
        if m < n:
            for i in range(m):
                result[i,:] = minkowski_distance(x[i],y,p)
        else:
            for j in range(n):
                result[:,j] = minkowski_distance(x,y[j],p)
        return result

