
def orth(A, rcond=None):
    """
    Construct an orthonormal basis for the range of A using SVD.

    Parameters
    ----------
    A : (M, N) array_like
        Input array
    rcond : float, optional
        Relative condition number. Singular values ``s`` smaller than
        ``rcond * max(s)`` are considered zero.
        Default: floating point eps * max(M,N).

    Returns
    -------
    Q : (M, K) ndarray
        Orthonormal basis for the range of A.
        K = effective rank of A, as determined by rcond

    See Also
    --------
    svd : Singular value decomposition of a matrix
    null_space : Matrix null space

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import orth
    >>> A = np.array([[2, 0, 0], [0, 5, 0]])  # rank 2 array
    >>> orth(A)
    array([[0., 1.],
           [1., 0.]])
    >>> orth(A.T)
    array([[0., 1.],
           [1., 0.],
           [0., 0.]])

    """
    u, s, vh = svd(A, full_matrices=False)
    M, N = u.shape[0], vh.shape[1]
    if rcond is None:
        rcond = np.finfo(s.dtype).eps * max(M, N)
    tol = np.amax(s, initial=0.) * rcond
    num = np.sum(s > tol, dtype=int)
    Q = u[:, :num]
    return Q

