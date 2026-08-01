
def eigsh(A, k=6, M=None, sigma=None, which='LM', v0=None,
          ncv=None, maxiter=None, tol=0, return_eigenvectors=True,
          Minv=None, OPinv=None, mode='normal', rng=None):
    """
    Find k eigenvalues and eigenvectors of the real symmetric square matrix
    or complex Hermitian matrix A.

    Solves ``A @ x[i] = w[i] * x[i]``, the standard eigenvalue problem for
    w[i] eigenvalues with corresponding eigenvectors x[i].

    If M is specified, solves ``A @ x[i] = w[i] * M @ x[i]``, the
    generalized eigenvalue problem for w[i] eigenvalues
    with corresponding eigenvectors x[i].

    Note that there is no specialized routine for the case when A is a complex
    Hermitian matrix. In this case, ``eigsh()`` will call ``eigs()`` and return
    the real parts of the eigenvalues thus obtained.

    Parameters
    ----------
    A : ndarray, sparse matrix or LinearOperator
        A square operator representing the operation ``A @ x``, where ``A`` is
        real symmetric or complex Hermitian. For buckling mode (see below)
        ``A`` must additionally be positive-definite.
    k : int, optional
        The number of eigenvalues and eigenvectors desired.
        `k` must be smaller than N. It is not possible to compute all
        eigenvectors of a matrix.

    Returns
    -------
    w : array
        Array of k eigenvalues.
    v : array
        An array representing the `k` eigenvectors.  The column ``v[:, i]`` is
        the eigenvector corresponding to the eigenvalue ``w[i]``.

    Other Parameters
    ----------------
    M : An N x N matrix, array, sparse matrix, or linear operator representing
        the operation ``M @ x`` for the generalized eigenvalue problem::

            A @ x = w * M @ x.

        M must represent a real symmetric matrix if A is real, and must
        represent a complex Hermitian matrix if A is complex. For best
        results, the data type of M should be the same as that of A.
        Additionally:

        - If sigma is None, M is symmetric positive definite.
        - If sigma is specified, M is symmetric positive semi-definite.
        - In buckling mode, M is symmetric indefinite.

        If sigma is None, eigsh requires an operator to compute the solution
        of the linear equation ``M @ x = b``. This is done internally via a
        (sparse) LU decomposition for an explicit matrix M, or via an
        iterative solver for a general linear operator.  Alternatively,
        the user can supply the matrix or operator Minv, which gives
        ``x = Minv @ b = M^-1 @ b``.
    sigma : real
        Find eigenvalues near sigma using shift-invert mode.  This requires
        an operator to compute the solution of the linear system
        ``[A - sigma * M] x = b``, where M is the identity matrix if
        unspecified.  This is computed internally via a (sparse) LU
        decomposition for explicit matrices A & M, or via an iterative
        solver if either A or M is a general linear operator.
        Alternatively, the user can supply the matrix or operator `OPinv`,
        which gives ``x = OPinv @ b = [A - sigma * M]^-1 @ b``.
        Regardless of the selected mode (normal, cayley, or buckling),
        `OPinv` should always be supplied as ``OPinv = [A - sigma * M]^-1``.

        Note that when sigma is specified, the keyword 'which' refers to
        the shifted eigenvalues ``w'[i]`` where:

        - if ``mode == 'normal'``: ``w'[i] = 1 / (w[i] - sigma)``.
        - if ``mode == 'cayley'``:  ``w'[i] = (w[i] + sigma) / (w[i] - sigma)``.
        - if ``mode == 'buckling'``: ``w'[i] = w[i] / (w[i] - sigma)``.

        (see further discussion in 'mode' below)
    which : str ['LM' | 'SM' | 'LA' | 'SA' | 'BE']
        If A is a complex Hermitian matrix, 'BE' is invalid.
        Which `k` eigenvectors and eigenvalues to find:

        - 'LM' : Largest (in magnitude) eigenvalues.
        - 'SM' : Smallest (in magnitude) eigenvalues.
        - 'LA' : Largest (algebraic) eigenvalues.
        - 'SA' : Smallest (algebraic) eigenvalues.
        - 'BE' : Half (k/2) from each end of the spectrum.

        When k is odd, return one more (k/2+1) from the high end.
        When sigma != None, 'which' refers to the shifted eigenvalues ``w'[i]``
        (see discussion in 'sigma', above).  ARPACK is generally better
        at finding large values than small values.  If small eigenvalues are
        desired, consider using shift-invert mode for better performance.
    v0 : ndarray, optional
        Starting vector for iteration. Default: random
    ncv : int, optional
        The number of Lanczos vectors generated ncv must be greater than k and
        smaller than n; it is recommended that ``ncv > 2*k``.
        Default: ``min(n, max(2*k + 1, 20))``
    maxiter : int, optional
        Maximum number of Arnoldi update iterations allowed.
        Default: ``n*10``
    tol : float
        Relative accuracy for eigenvalues (stopping criterion).
        The default value of 0 implies machine precision.
    return_eigenvectors : bool
        Return eigenvectors (True) in addition to eigenvalues.
        This value determines the order in which eigenvalues are sorted.
        The sort order is also dependent on the `which` variable.

        - For which = 'LM' or 'SA':

          - If `return_eigenvectors` is True, eigenvalues are sorted by
            algebraic value.
          - If `return_eigenvectors` is False, eigenvalues are sorted by
            absolute value.

        - For which = 'BE' or 'LA':

          - eigenvalues are always sorted by algebraic value.

        - For which = 'SM':

          - If `return_eigenvectors` is True, eigenvalues are sorted by
            algebraic value.
          - If `return_eigenvectors` is False, eigenvalues are sorted by
            decreasing absolute value.

    Minv : N x N matrix, array, sparse matrix, or LinearOperator
        See notes in M, above.
    OPinv : N x N matrix, array, sparse matrix, or LinearOperator
        See notes in sigma, above.
    mode : str ['normal' | 'buckling' | 'cayley']
        Specify strategy to use for shift-invert mode.  This argument applies
        only for real-valued A and sigma != None.  For shift-invert mode,
        ARPACK internally solves the eigenvalue problem
        ``OP @ x'[i] = w'[i] * B @ x'[i]``
        and transforms the resulting Ritz vectors x'[i] and Ritz values w'[i]
        into the desired eigenvectors and eigenvalues of the problem
        ``A @ x[i] = w[i] * M @ x[i]``.
        The modes are as follows:

        - 'normal'::

            OP = [A - sigma * M]^-1 @ M,
            B = M,
            w'[i] = 1 / (w[i] - sigma)

        - 'buckling'::

            OP = [A - sigma * M]^-1 @ A,
            B = A,
            w'[i] = w[i] / (w[i] - sigma)

        - 'cayley'::

            OP = [A - sigma * M]^-1 @ [A + sigma * M],
            B = M,
            w'[i] = (w[i] + sigma) / (w[i] - sigma)

        The choice of mode will affect which eigenvalues are selected by
        the keyword 'which', and can also impact the stability of
        convergence (see [2]_ for a discussion).
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.

        .. versionadded:: 1.17.0

    Raises
    ------
    ArpackNoConvergence
        When the requested convergence is not obtained.

        The currently converged eigenvalues and eigenvectors can be found
        as ``eigenvalues`` and ``eigenvectors`` attributes of the exception
        object.

    See Also
    --------
    eigs : eigenvalues and eigenvectors for a general (nonsymmetric) matrix A
    svds : singular value decomposition for a matrix A

    Notes
    -----
    This function is a wrapper to the ARPACK [1]_ SSEUPD and DSEUPD
    functions which use the Implicitly Restarted Lanczos Method to
    find the eigenvalues and eigenvectors [2]_.

    References
    ----------
    .. [1] ARPACK Software, https://github.com/opencollab/arpack-ng
    .. [2] R. B. Lehoucq, D. C. Sorensen, and C. Yang,  ARPACK USERS GUIDE:
       Solution of Large Scale Eigenvalue Problems by Implicitly Restarted
       Arnoldi Methods. SIAM, Philadelphia, PA, 1998.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.sparse.linalg import eigsh
    >>> identity = np.eye(13)
    >>> eigenvalues, eigenvectors = eigsh(identity, k=6)
    >>> eigenvalues
    array([1., 1., 1., 1., 1., 1.])
    >>> eigenvectors.shape
    (13, 6)

    """
    # complex Hermitian matrices should be solved with eigs
    if np.issubdtype(A.dtype, np.complexfloating):
        if mode != 'normal':
            raise ValueError(f"mode={mode} cannot be used with complex matrix A")
        if which == 'BE':
            raise ValueError("which='BE' cannot be used with complex matrix A")
        elif which == 'LA':
            which = 'LR'
        elif which == 'SA':
            which = 'SR'
        ret = eigs(A, k, M=M, sigma=sigma, which=which, v0=v0,
                   ncv=ncv, maxiter=maxiter, tol=tol,
                   return_eigenvectors=return_eigenvectors, Minv=Minv,
                   OPinv=OPinv)

        if return_eigenvectors:
            return ret[0].real, ret[1]
        else:
            return ret.real

    if (A_ndim := len(A.shape)) > 2:
        raise ValueError(f"{A_ndim}-dimensional `A` is unsupported, expected 2-D.")
    if A.shape[0] != A.shape[1]:
        raise ValueError(f'expected square matrix (shape={A.shape})')
    if M is not None:
        if M.shape != A.shape:
            raise ValueError(f'wrong M dimensions {M.shape}, should be {A.shape}')
        if np.dtype(M.dtype).char.lower() != np.dtype(A.dtype).char.lower():
            warnings.warn('M does not have the same type precision as A. '
                          'This may adversely affect ARPACK convergence',
                          stacklevel=2)

    n = A.shape[0]

    if k <= 0:
        raise ValueError("k must be greater than 0.")

    if k >= n:
        warnings.warn("k >= N for N * N square matrix. "
                      "Attempting to use scipy.linalg.eigh instead.",
                      RuntimeWarning, stacklevel=2)

        if issparse(A):
            raise TypeError("Cannot use scipy.linalg.eigh for sparse A with "
                            "k >= N. Use scipy.linalg.eigh(A.toarray()) or"
                            " reduce k.")
        if isinstance(A, LinearOperator):
            raise TypeError("Cannot use scipy.linalg.eigh for LinearOperator "
                            "A with k >= N.")
        if isinstance(M, LinearOperator):
            raise TypeError("Cannot use scipy.linalg.eigh for LinearOperator "
                            "M with k >= N.")

        return eigh(A, b=M, eigvals_only=not return_eigenvectors)

    if sigma is None:
        A = aslinearoperator(A)
        matvec = A.matvec

        if OPinv is not None:
            raise ValueError("OPinv should not be specified with sigma = None.")
        if M is None:
            #standard eigenvalue problem
            mode = 1
            M_matvec = None
            Minv_matvec = None
            if Minv is not None:
                raise ValueError("Minv should not be specified with M = None.")
        else:
            #general eigenvalue problem
            mode = 2
            if Minv is None:
                Minv_matvec = get_inv_matvec(M, hermitian=True, tol=tol)
            else:
                Minv = aslinearoperator(Minv)
                Minv_matvec = Minv.matvec
            M_matvec = aslinearoperator(M).matvec
    else:
        # sigma is not None: shift-invert mode
        if Minv is not None:
            raise ValueError("Minv should not be specified when sigma is "
                             "specified.")

        # normal mode
        if mode == 'normal':
            mode = 3
            matvec = None
            if OPinv is None:
                Minv_matvec = get_OPinv_matvec(A, M, sigma,
                                               hermitian=True, tol=tol)
            else:
                OPinv = aslinearoperator(OPinv)
                Minv_matvec = OPinv.matvec
            if M is None:
                M_matvec = None
            else:
                M = aslinearoperator(M)
                M_matvec = M.matvec

        # buckling mode
        elif mode == 'buckling':
            mode = 4
            if OPinv is None:
                Minv_matvec = get_OPinv_matvec(A, M, sigma,
                                               hermitian=True, tol=tol)
            else:
                Minv_matvec = aslinearoperator(OPinv).matvec
            matvec = aslinearoperator(A).matvec
            M_matvec = None

        # cayley-transform mode
        elif mode == 'cayley':
            mode = 5
            matvec = aslinearoperator(A).matvec
            if OPinv is None:
                Minv_matvec = get_OPinv_matvec(A, M, sigma,
                                               hermitian=True, tol=tol)
            else:
                Minv_matvec = aslinearoperator(OPinv).matvec
            if M is None:
                M_matvec = None
            else:
                M_matvec = aslinearoperator(M).matvec

        # unrecognized mode
        else:
            raise ValueError(f"unrecognized mode '{mode}'")
    rng = np.random.default_rng(rng)
    params = _SymmetricArpackParams(n, k, A.dtype.char, matvec, mode,
                                    M_matvec, Minv_matvec, sigma,
                                    ncv, v0, maxiter, which, tol, rng)

    while not params.converged:
        params.iterate()

    return params.extract(return_eigenvectors)

