
def fractional_matrix_power(A, t):
    """
    Compute the fractional power of a matrix.

    Proceeds according to the discussion in section (6) of [1]_.

    Parameters
    ----------
    A : (N, N) array_like
        Matrix whose fractional power to evaluate.
    t : float
        Fractional power.

    Returns
    -------
    X : (N, N) array_like
        The fractional power of the matrix.

    References
    ----------
    .. [1] Nicholas J. Higham and Lijing Lin (2011)
           "A Schur-Pade Algorithm for Fractional Powers of a Matrix."
           SIAM Journal on Matrix Analysis and Applications,
           32 (3). pp. 1056-1078. ISSN 0895-4798.
           :doi:`10.1137/10081232X`

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import fractional_matrix_power
    >>> a = np.array([[1.0, 3.0], [1.0, 4.0]])
    >>> b = fractional_matrix_power(a, 0.5)
    >>> b
    array([[ 0.75592895,  1.13389342],
           [ 0.37796447,  1.88982237]])
    >>> np.dot(b, b)      # Verify square root
    array([[ 1.,  3.],
           [ 1.,  4.]])

    """
    # This fixes some issue with imports;
    # this function calls onenormest which is in scipy.sparse.
    A = _asarray_square(A)
    import scipy.linalg._matfuncs_inv_ssq
    return scipy.linalg._matfuncs_inv_ssq._fractional_matrix_power(A, t)

