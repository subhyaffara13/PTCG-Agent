
def funm_multiply_krylov(f, A, b, *, assume_a = "general", t = 1.0, atol = 0.0,
                         rtol = 1e-6, restart_every_m = None, max_restarts = 20):
    """
    A restarted Krylov method for evaluating ``y = f(tA) b`` from [1]_ [2]_.

    Parameters
    ----------
    f : callable
        Callable object that computes the matrix function ``F = f(X)``.
    A : {sparse array, ndarray, LinearOperator}
        A real or complex N-by-N matrix.
        Alternatively, `A` can be a linear operator which can
        produce ``Ax`` using, e.g., ``scipy.sparse.linalg.LinearOperator``.
    b : ndarray
        A vector to multiply the ``f(tA)`` with.
    assume_a : str, optional
        Indicate the structure of ``A``. The algorithm will use this information
        to select the appropriated code path. The available options are
        'hermitian'/'her' and 'general'/'gen'. If ommited, then it is assumed
        that ``A`` has a 'general' structure.
    t : float, optional
        The value to scale the matrix ``A`` with. The default is ``t = 1.0``
    atol, rtol : float, optional
        Parameters for the convergence test. For convergence,
        ``norm(||y_k - y_k-1||) <= max(rtol*norm(b), atol)`` should be satisfied.
        The default is ``atol=0.`` and ``rtol=1e-6``.
    restart_every_m : int
        If the iteration number reaches this value a restart is triggered.
        Larger values increase iteration cost but may be necessary for convergence.
        If omitted, ``min(20, n)`` is used.
    max_restarts : int, optional
        Maximum number of restart cycles. The algorithm will stop
        after max_restarts cycles even if the specified tolerance has not been
        achieved. The default is ``max_restarts=20``

    Returns
    -------
    y : ndarray
        The result of ``f(tA) b``.

    Notes
    -----
    The convergence of the Krylov method heavily depends on the spectrum
    of ``A`` and the function ``f``. With restarting, there are only formal
    proofs for functions of order 1 (e.g., ``exp``, ``sin``, ``cos``) and
    Stieltjes functions [2]_ [3]_, while the general case remains an open problem.

    References
    ----------
    .. [1] M. Afanasjew, M. Eiermann, O. G. Ernst, and S. Güttel,
           "Implementation of a restarted Krylov subspace method for the
           evaluation of matrix functions," Linear Algebra and its Applications,
           vol. 429, no. 10, pp. 2293-2314, Nov. 2008, :doi:`10.1016/j.laa.2008.06.029`.

    .. [2] M. Eiermann and O. G. Ernst, "A Restarted Krylov Subspace Method
           for the Evaluation of Matrix Functions," SIAM J. Numer. Anal., vol. 44,
           no. 6, pp. 2481-2504, Jan. 2006, :doi:`10.1137/050633846`.

    .. [3] A. Frommer, S. Güttel, and M. Schweitzer, "Convergence of Restarted
           Krylov Subspace Methods for Stieltjes Functions of Matrices," SIAM J.
           Matrix Anal. Appl., vol. 35, no. 4, pp. 1602-1624,
           Jan. 2014, :doi:`10.1137/140973463`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse import csr_array
    >>> from scipy.sparse.linalg import funm_multiply_krylov
    >>> from scipy.linalg import expm, solve
    >>> A = csr_array([[3, 2, 0], [1, -1, 0], [0, 5, 1]], dtype=float)
    >>> b = np.array([2, 4, -1], dtype=float)
    >>> t = 0.1

    Compute ``y = exp(tA) b``.

    >>> y = funm_multiply_krylov(expm, A, b, t = t)
    >>> y
    array([3.6164913 , 3.88421511 , 0.96073457])

    >>> ref = expm(t * A.todense()) @ b
    >>> err = y - ref
    >>> err
    array([4.44089210e-16 , 0.00000000e+00 , 2.22044605e-16])

    Compute :math:`y = (A^3 - A) b`.

    >>> poly = lambda X : X @ X @ X - X
    >>> y = funm_multiply_krylov(poly, A, b)
    >>> y
    array([132. , 24. , 70.])

    >>> ref = poly(A.todense()) @ b
    >>> err = y - ref
    >>> err
    array([ 0.00000000e+00 , 7.10542736e-15 , -2.84217094e-14])

    Compute :math:`y = f(tA) b`, where  :math:`f(X) = X^{-1}(e^{X} - I)`. This is
    known as the "phi function" from the exponential integrator literature.

    >>> phim_1 = lambda X : solve(X, expm(X) - np.eye(X.shape[0]))
    >>> y = funm_multiply_krylov(phim_1, A, b, t = t)
    >>> y
    array([ 2.76984306 , 3.92769192 , -0.03111392])

    >>> ref = phim_1(t * A.todense()) @ b
    >>> err = y - ref
    >>> err
    array([ 0.00000000e+00 , 8.88178420e-16 , -4.60742555e-15])
    """

    if assume_a not in {'hermitian', 'general', 'her', 'gen'}:
        raise ValueError(f'scipy.sparse.linalg.funm_multiply_krylov: {assume_a} '
                         'is not a recognized matrix structure')
    is_hermitian = (assume_a == 'her') or (assume_a == 'hermitian')

    if len(b.shape) != 1:
        raise ValueError("scipy.sparse.linalg.funm_multiply_krylov: "
                         "argument 'b' must be a 1D array.")
    n = b.shape[0]

    if restart_every_m is None:
        restart_every_m = min(20, n)

    restart_every_m = int(restart_every_m)
    max_restarts = int(max_restarts)

    if restart_every_m <= 0:
        raise ValueError("scipy.sparse.linalg.funm_multiply_krylov: "
                         "argument 'restart_every_m' must be positive.")

    if max_restarts <= 0:
            raise ValueError("scipy.sparse.linalg.funm_multiply_krylov: "
                             "argument 'max_restarts' must be positive.")

    m = restart_every_m
    max_restarts = min(max_restarts, int(n / m) + 1)
    mmax = m * max_restarts

    bnorm = norm(b)
    atol, _ = _get_atol_rtol("funm_multiply_krylov", bnorm, atol, rtol)

    if bnorm == 0:
        y = np.array(b)
        return y

    # Preallocate the maximum memory space.
    # Using the column major order here since we work with
    # each individual column separately.
    internal_type = np.common_type(A, b)
    V = np.zeros((n, m + 1), dtype = internal_type, order = 'F')
    H = np.zeros((mmax + 1, mmax), dtype = internal_type, order = 'F')

    restart = 1

    if is_hermitian:
        breakdown, j = _funm_multiply_krylov_lanczos(A, b, bnorm, V,
                                                        H[:m + 1, :m], m)
    else:
        breakdown, j = _funm_multiply_krylov_arnoldi(A, b, bnorm, V,
                                                        H[:m + 1, :m], m)

    fH = f(t * H[:j, :j])
    y = bnorm * V[:, :j].dot(fH[:, 0])

    if breakdown:
        return y

    update_norm = norm(bnorm * fH[:, 0])

    while restart < max_restarts and update_norm > atol:
        begin = restart * m
        end = (restart + 1) * m

        if is_hermitian:
            breakdown, j = _funm_multiply_krylov_lanczos(A, V[:, m], 1, V,
                                                         H[begin:end + 1, begin:end], m)
        else:
            breakdown, j = _funm_multiply_krylov_arnoldi(A, V[:, m], 1, V,
                                                         H[begin:end + 1, begin:end], m)

        if breakdown:
            end = begin + j
            fH = f(t * H[:end, :end])
            y[:end] = y[:end] + bnorm * V[:, :m].dot(fH[begin:end, 0])
            return y

        fH = f(t * H[:end, :end])
        y = y + bnorm * V[:, :m].dot(fH[begin:end, 0])
        update_norm = norm(bnorm * fH[begin:end, 0])
        restart += 1

    return y

