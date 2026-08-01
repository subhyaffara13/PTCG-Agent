
def null_space(A, rcond=None, *, overwrite_a=False, check_finite=True,
               lapack_driver='gesdd'):
    """
    Construct an orthonormal basis for the null space of A using SVD.

    Parameters
    ----------
    A : (M, N) array_like
        Input array
    rcond : float, optional
        Relative condition number. Singular values ``s`` smaller than
        ``rcond * max(s)`` are considered zero.
        Default: floating point eps * max(M,N).
    overwrite_a : bool, optional
        Whether to overwrite `a`; may improve performance. Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    lapack_driver : {'gesdd', 'gesvd'}, optional
        Whether to use the more efficient divide-and-conquer approach
        (``'gesdd'``) or general rectangular approach (``'gesvd'``)
        to compute the SVD. MATLAB and Octave use the ``'gesvd'`` approach.
        Default is ``'gesdd'``.

    Returns
    -------
    Z : (N, K) ndarray
        Orthonormal basis for the null space of A.
        K = dimension of effective null space, as determined by rcond

    See Also
    --------
    svd : Singular value decomposition of a matrix
    orth : Matrix range

    Examples
    --------
    1-D null space:

    >>> import numpy as np
    >>> from scipy.linalg import null_space
    >>> A = np.array([[1, 1], [1, 1]])
    >>> ns = null_space(A)
    >>> ns * np.copysign(1, ns[0,0])  # Remove the sign ambiguity of the vector
    array([[ 0.70710678],
           [-0.70710678]])

    2-D null space:

    >>> from numpy.random import default_rng
    >>> rng = default_rng()
    >>> B = rng.random((3, 5))
    >>> Z = null_space(B)
    >>> Z.shape
    (5, 2)
    >>> np.allclose(B.dot(Z), 0)
    True

    The basis vectors are orthonormal (up to rounding error):

    >>> Z.T.dot(Z)
    array([[  1.00000000e+00,   6.92087741e-17],
           [  6.92087741e-17,   1.00000000e+00]])

    """
    u, s, vh = svd(A, full_matrices=True, overwrite_a=overwrite_a,
                   check_finite=check_finite, lapack_driver=lapack_driver)
    M, N = u.shape[0], vh.shape[1]
    if rcond is None:
        rcond = np.finfo(s.dtype).eps * max(M, N)
    tol = np.amax(s, initial=0.) * rcond
    num = np.sum(s > tol, dtype=int)
    Q = vh[num:,:].T.conj()
    return Q

