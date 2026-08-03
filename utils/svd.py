from typing import Any

def svd(a: ArrayLike, full_matrices=True, compute_uv=True, hermitian=False):
    a = _atleast_float_1(a)
    if not compute_uv:
        return torch.linalg.svdvals(a)

    # NB: ignore the hermitian= argument (no pytorch equivalent)
    result = torch.linalg.svd(a, full_matrices=full_matrices)
    return result


def svd(A: TensorLikeType, full_matrices: bool = True) -> tuple[Tensor, Tensor, Tensor]:
    return prims.svd(A, full_matrices=full_matrices)


def svd(expr):
    return UofSVD(expr), SofSVD(expr), VofSVD(expr)


def svd(A, eps_or_k, rand=True, rng=None):
    """
    Compute SVD of a matrix via an ID.

    An SVD of a matrix `A` is a factorization::

        A = U @ np.diag(S) @ V.conj().T

    where `U` and `V` have orthonormal columns and `S` is nonnegative.

    The SVD can be computed to any relative precision or rank (depending on the
    value of `eps_or_k`).

    See also :func:`interp_decomp` and :func:`id_to_svd`.

    ..  This function automatically detects the form of the input parameters and
        passes them to the appropriate backend. For details, see
        :func:`_backend.iddp_svd`, :func:`_backend.iddp_asvd`,
        :func:`_backend.iddp_rsvd`, :func:`_backend.iddr_svd`,
        :func:`_backend.iddr_asvd`, :func:`_backend.iddr_rsvd`,
        :func:`_backend.idzp_svd`, :func:`_backend.idzp_asvd`,
        :func:`_backend.idzp_rsvd`, :func:`_backend.idzr_svd`,
        :func:`_backend.idzr_asvd`, and :func:`_backend.idzr_rsvd`.

    Parameters
    ----------
    A : :class:`numpy.ndarray` or :class:`scipy.sparse.linalg.LinearOperator`
        Matrix to be factored, given as either a :class:`numpy.ndarray` or a
        :class:`scipy.sparse.linalg.LinearOperator` with the `matvec` and
        `rmatvec` methods (to apply the matrix and its adjoint).
    eps_or_k : float or int
        Relative error (if ``eps_or_k < 1``) or rank (if ``eps_or_k >= 1``) of
        approximation.
    rand : bool, optional
        Whether to use random sampling if `A` is of type :class:`numpy.ndarray`
        (randomized algorithms are always used if `A` is of type
        :class:`scipy.sparse.linalg.LinearOperator`).
    rng : `numpy.random.Generator`, optional
        Pseudorandom number generator state. When `rng` is None, a new
        `numpy.random.Generator` is created using entropy from the
        operating system. Types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.
        If `rand` is ``False``, the argument is ignored.

    Returns
    -------
    U : :class:`numpy.ndarray`
        2D array of left singular vectors.
    S : :class:`numpy.ndarray`
        1D array of singular values.
    V : :class:`numpy.ndarray`
        2D array right singular vectors.
    """
    from scipy.sparse.linalg import LinearOperator
    rng = np.random.default_rng(rng)

    real = _is_real(A)

    if isinstance(A, np.ndarray):
        A = _C_contiguous_copy(A)
        if eps_or_k < 1:
            eps = eps_or_k
            if rand:
                if real:
                    U, S, V = _backend.iddp_asvd(A, eps, rng=rng)
                else:
                    U, S, V = _backend.idzp_asvd(A, eps, rng=rng)
            else:
                if real:
                    U, S, V = _backend.iddp_svd(A, eps)
                    V = V.T.conj()
                else:
                    U, S, V = _backend.idzp_svd(A, eps)
                    V = V.T.conj()
        else:
            k = int(eps_or_k)
            if k > min(A.shape):
                raise ValueError(f"Approximation rank {k} exceeds min(A.shape) = "
                                 f" {min(A.shape)} ")
            if rand:
                if real:
                    U, S, V = _backend.iddr_asvd(A, k, rng=rng)
                else:
                    U, S, V = _backend.idzr_asvd(A, k, rng=rng)
            else:
                if real:
                    U, S, V = _backend.iddr_svd(A, k)
                    V = V.T.conj()
                else:
                    U, S, V = _backend.idzr_svd(A, k)
                    V = V.T.conj()
    elif isinstance(A, LinearOperator):
        if eps_or_k < 1:
            eps = eps_or_k
            if real:
                U, S, V = _backend.iddp_rsvd(A, eps, rng=rng)
            else:
                U, S, V = _backend.idzp_rsvd(A, eps, rng=rng)
        else:
            k = int(eps_or_k)
            if real:
                U, S, V = _backend.iddr_rsvd(A, k, rng=rng)
            else:
                U, S, V = _backend.idzr_rsvd(A, k, rng=rng)
    else:
        raise _TYPE_ERROR
    return U, S, V


def svd(a, full_matrices=True, compute_uv=True, overwrite_a=False,
        check_finite=True, lapack_driver='gesdd'):
    """
    Singular Value Decomposition.

    Factorizes the matrix `a` into two unitary matrices ``U`` and ``Vh``, and
    a 1-D array ``s`` of singular values (real, non-negative) such that
    ``a == U @ S @ Vh``, where ``S`` is a suitably shaped matrix of zeros with
    main diagonal ``s``.

    Parameters
    ----------
    a : (..., M, N) array_like
        Matrix to decompose.
    full_matrices : bool, optional
        If True (default), `U` and `Vh` are of shape ``(M, M)``, ``(N, N)``.
        If False, the shapes are ``(M, K)`` and ``(K, N)``, where
        ``K = min(M, N)``.
    compute_uv : bool, optional
        Whether to compute also ``U`` and ``Vh`` in addition to ``s``.
        Default is True.
    overwrite_a : bool, optional
        Whether to overwrite data in `a` (may improve performance). Default is False.
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
    U : ndarray
        Unitary matrix having left singular vectors as columns.
        Of shape ``(M, M)`` or ``(M, K)``, depending on `full_matrices`.
        Only present when ``compute_uv=True``.
    s : ndarray
        The singular values, sorted in non-increasing order.
        Of shape (K,), with ``K = min(M, N)``.
    Vh : ndarray
        Unitary matrix having right singular vectors as rows.
        Of shape ``(N, N)`` or ``(K, N)`` depending on `full_matrices`.
        Only present when ``compute_uv=True``.

    Raises
    ------
    LinAlgError
        If SVD computation does not converge.

    See Also
    --------
    svdvals : Compute singular values of a matrix.
    diagsvd : Construct the Sigma matrix, given the vector s.

    Notes
    -----
    The array argument of this function, `a`, may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import linalg
    >>> rng = np.random.default_rng()
    >>> m, n = 9, 6
    >>> a = rng.standard_normal((m, n)) + 1.j*rng.standard_normal((m, n))
    >>> U, s, Vh = linalg.svd(a)
    >>> U.shape,  s.shape, Vh.shape
    ((9, 9), (6,), (6, 6))

    Reconstruct the original matrix from the decomposition:

    >>> sigma = np.zeros((m, n))
    >>> for i in range(min(m, n)):
    ...     sigma[i, i] = s[i]
    >>> a1 = U @ sigma @ Vh
    >>> np.allclose(a, a1)
    True

    Alternatively, use ``full_matrices=False`` (notice that the shape of
    ``U`` is then ``(m, n)`` instead of ``(m, m)``):

    >>> U, s, Vh = linalg.svd(a, full_matrices=False)
    >>> U.shape, s.shape, Vh.shape
    ((9, 6), (6,), (6, 6))
    >>> S = np.diag(s)
    >>> np.allclose(a, U @ S @ Vh)
    True

    >>> s2 = linalg.svd(a, compute_uv=False)
    >>> np.allclose(s, s2)
    True

    If the input matrix has more than two dimensions, it is interpreted as a batch of
    two-dimensional matrices:

    >>> aa = np.stack((a, 2*a))
    >>> linalg.svdvals(aa)[0] == linalg.svdvals(a)
    array([ True,  True,  True,  True,  True,  True])
    >>> linalg.svdvals(aa)[1] == 2 * linalg.svdvals(a)
    array([ True,  True,  True,  True,  True,  True])
    """
    if not isinstance(lapack_driver, str):
        raise TypeError('lapack_driver must be a string')
    if lapack_driver not in ('gesdd', 'gesvd'):
        message = f'lapack_driver must be "gesdd" or "gesvd", not "{lapack_driver}"'
        raise ValueError(message)

    # basic sanity checks of the input matrix
    a1 = _asarray_validated(a, check_finite=check_finite)
    _deprecate_dtypes("svd", a1)

    if a1.ndim < 2:
        raise ValueError(f"Expected at least ndim=2, got {a1.ndim=}")

    m, n = a1.shape[-2], a1.shape[-1]

    # Also check if dtype is LAPACK compatible
    a1, overwrite_a = _normalize_lapack_dtype(a1, overwrite_a)
    a1, overwrite_a = _ensure_aligned_and_native(a1, overwrite_a)

    overwrite_a = overwrite_a or (_datacopied(a1, a))
    overwrite_a = overwrite_a and (a1.ndim == 2) and (a1.flags["F_CONTIGUOUS"])

    # accommodate empty matrix
    if a1.size == 0:
        u0, s0, v0 = svd(np.eye(2, dtype=a1.dtype))

        batch_shape = a1.shape[:-2]
        s = np.empty_like(a1, shape=batch_shape + (0,), dtype=s0.dtype)
        if full_matrices:
            u = np.empty_like(a1, shape=batch_shape + (m, m), dtype=u0.dtype)
            u[...] = np.identity(m)
            v = np.empty_like(a1, shape=batch_shape + (n, n), dtype=v0.dtype)
            v[...] = np.identity(n)
        else:
            u = np.empty_like(a1, shape=batch_shape + (m, 0), dtype=u0.dtype)
            v = np.empty_like(a1, shape=batch_shape + (0, n), dtype=v0.dtype)
        if compute_uv:
            return u, s, v
        else:
            return s

    if compute_uv:
        max_mn, min_mn = (m, n) if m > n else (n, m)
        if full_matrices:
            if not HAS_ILP64 and max_mn*max_mn > np.iinfo(np.int32).max:
                raise ValueError(f"Indexing a matrix size {max_mn} x {max_mn} "
                                  "would incur integer overflow in LAPACK. "
                                  "Instead, either use using numpy.linalg.svd or build"
                                  "SciPy with ILP64 support.")
        else:
            sz = max(m * min_mn, n * min_mn)
            if not HAS_ILP64 and max(m * min_mn, n * min_mn) > np.iinfo(np.int32).max:
                raise ValueError(f"Indexing a matrix of {sz} elements would "
                                  "incur an in integer overflow in LAPACK. "
                                  "Instead, either use using numpy.linalg.svd or build"
                                  "SciPy with ILP64 support.")

    res = _batched_linalg._svd(
        a1, lapack_driver, compute_uv, full_matrices, overwrite_a
    )

    err_lst = res[-1]
    if err_lst:
        _format_emit_errors_warnings(err_lst, lapack_driver)

    if compute_uv:
        return res[:-1]    # u, s, v
    else:
        return res[0]   # s


def svd(
    x: Array,
    /,
    xp: Namespace,
    *,
    full_matrices: bool = True,
    **kwargs: object,
) -> SVDResult:
    return SVDResult(*xp.linalg.svd(x, full_matrices=full_matrices, **kwargs))


def svd(x: Array, full_matrices: bool = True, **kwargs: object) -> SVDResult:  # type: ignore[no-redef]
    if full_matrices:
        raise ValueError("full_matrices=True is not supported by dask.")
    return da.linalg.svd(x, coerce_signs=False, **kwargs)


def svd(a, full_matrices=True, compute_uv=True, hermitian=False):
    """
    Singular Value Decomposition.

    When `a` is a 2D array, and ``full_matrices=False``, then it is
    factorized as ``u @ np.diag(s) @ vh = (u * s) @ vh``, where
    `u` and the Hermitian transpose of `vh` are 2D arrays with
    orthonormal columns and `s` is a 1D array of `a`'s singular
    values. When `a` is higher-dimensional, SVD is applied in
    stacked mode as explained below.

    Parameters
    ----------
    a : (..., M, N) array_like
        A real or complex array with ``a.ndim >= 2``.
    full_matrices : bool, optional
        If True (default), `u` and `vh` have the shapes ``(..., M, M)`` and
        ``(..., N, N)``, respectively.  Otherwise, the shapes are
        ``(..., M, K)`` and ``(..., K, N)``, respectively, where
        ``K = min(M, N)``.
    compute_uv : bool, optional
        Whether or not to compute `u` and `vh` in addition to `s`.  True
        by default.
    hermitian : bool, optional
        If True, `a` is assumed to be Hermitian (symmetric if real-valued),
        enabling a more efficient method for finding singular values.
        Defaults to False.

    Returns
    -------
    U : { (..., M, M), (..., M, K) } array
        Unitary array(s). The first ``a.ndim - 2`` dimensions have the same
        size as those of the input `a`. The size of the last two dimensions
        depends on the value of `full_matrices`. Only returned when
        `compute_uv` is True.
    S : (..., K) array
        Vector(s) with the singular values, within each vector sorted in
        descending order. The first ``a.ndim - 2`` dimensions have the same
        size as those of the input `a`.
    Vh : { (..., N, N), (..., K, N) } array
        Unitary array(s). The first ``a.ndim - 2`` dimensions have the same
        size as those of the input `a`. The size of the last two dimensions
        depends on the value of `full_matrices`. Only returned when
        `compute_uv` is True.

    Raises
    ------
    LinAlgError
        If SVD computation does not converge.

    See Also
    --------
    scipy.linalg.svd : Similar function in SciPy.
    scipy.linalg.svdvals : Compute singular values of a matrix.

    Notes
    -----
    When `compute_uv` is True, the result is a namedtuple with the following
    attribute names: `U`, `S`, and `Vh`.

    The decomposition is performed using LAPACK routine ``_gesdd``.

    SVD is usually described for the factorization of a 2D matrix :math:`A`.
    The higher-dimensional case will be discussed below. In the 2D case, SVD is
    written as :math:`A = U S V^H`, where :math:`A = a`, :math:`U= u`,
    :math:`S= \\mathtt{np.diag}(s)` and :math:`V^H = vh`. The 1D array `s`
    contains the singular values of `a` and `u` and `vh` are unitary. The rows
    of `vh` are the eigenvectors of :math:`A^H A` and the columns of `u` are
    the eigenvectors of :math:`A A^H`. In both cases the corresponding
    (possibly non-zero) eigenvalues are given by ``s**2``.

    If `a` has more than two dimensions, then broadcasting rules apply, as
    explained in :ref:`routines.linalg-broadcasting`. This means that SVD is
    working in "stacked" mode: it iterates over all indices of the first
    ``a.ndim - 2`` dimensions and for each combination SVD is applied to the
    last two indices. The matrix `a` can be reconstructed from the
    decomposition with either ``(u * s[..., None, :]) @ vh`` or
    ``u @ (s[..., None] * vh)``. (The ``@`` operator can be replaced by the
    function ``np.matmul`` for python versions below 3.5.)

    If `a` is a ``matrix`` object (as opposed to an ``ndarray``), then so are
    all the return values.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng()
    >>> a = rng.normal(size=(9, 6)) + 1j*rng.normal(size=(9, 6))
    >>> b = rng.normal(size=(2, 7, 8, 3)) + 1j*rng.normal(size=(2, 7, 8, 3))


    Reconstruction based on full SVD, 2D case:

    >>> U, S, Vh = np.linalg.svd(a, full_matrices=True)
    >>> U.shape, S.shape, Vh.shape
    ((9, 9), (6,), (6, 6))
    >>> np.allclose(a, np.dot(U[:, :6] * S, Vh))
    True
    >>> smat = np.zeros((9, 6), dtype=np.complex128)
    >>> smat[:6, :6] = np.diag(S)
    >>> np.allclose(a, np.dot(U, np.dot(smat, Vh)))
    True

    Reconstruction based on reduced SVD, 2D case:

    >>> U, S, Vh = np.linalg.svd(a, full_matrices=False)
    >>> U.shape, S.shape, Vh.shape
    ((9, 6), (6,), (6, 6))
    >>> np.allclose(a, np.dot(U * S, Vh))
    True
    >>> smat = np.diag(S)
    >>> np.allclose(a, np.dot(U, np.dot(smat, Vh)))
    True

    Reconstruction based on full SVD, 4D case:

    >>> U, S, Vh = np.linalg.svd(b, full_matrices=True)
    >>> U.shape, S.shape, Vh.shape
    ((2, 7, 8, 8), (2, 7, 3), (2, 7, 3, 3))
    >>> np.allclose(b, np.matmul(U[..., :3] * S[..., None, :], Vh))
    True
    >>> np.allclose(b, np.matmul(U[..., :3], S[..., None] * Vh))
    True

    Reconstruction based on reduced SVD, 4D case:

    >>> U, S, Vh = np.linalg.svd(b, full_matrices=False)
    >>> U.shape, S.shape, Vh.shape
    ((2, 7, 8, 3), (2, 7, 3), (2, 7, 3, 3))
    >>> np.allclose(b, np.matmul(U * S[..., None, :], Vh))
    True
    >>> np.allclose(b, np.matmul(U, S[..., None] * Vh))
    True

    """
    import numpy as np
    a, wrap = _makearray(a)

    if hermitian:
        # note: lapack svd returns eigenvalues with s ** 2 sorted descending,
        # but eig returns s sorted ascending, so we re-order the eigenvalues
        # and related arrays to have the correct order
        if compute_uv:
            s, u = eigh(a)
            # avoid zero sign
            sgn = np.copysign(1.0, s)
            s = abs(s)
            sidx = argsort(s)[..., ::-1]
            sgn = np.take_along_axis(sgn, sidx, axis=-1)
            s = np.take_along_axis(s, sidx, axis=-1)
            u = np.take_along_axis(u, sidx[..., None, :], axis=-1)
            # singular values are unsigned, move the sign into v
            vt = transpose(u * sgn[..., None, :]).conjugate()
            return SVDResult(wrap(u), s, wrap(vt))
        else:
            s = eigvalsh(a)
            s = abs(s)
            return sort(s)[..., ::-1]

    _assert_stacked_2d(a)
    t, result_t = _commonType(a)

    m, n = a.shape[-2:]
    if compute_uv:
        if full_matrices:
            gufunc = _umath_linalg.svd_f
        else:
            gufunc = _umath_linalg.svd_s

        signature = 'D->DdD' if isComplexType(t) else 'd->ddd'
        with errstate(call=_raise_linalgerror_svd_nonconvergence,
                      invalid='call', over='ignore', divide='ignore',
                      under='ignore'):
            u, s, vh = gufunc(a, signature=signature)
        u = u.astype(result_t, copy=False)
        s = s.astype(_realType(result_t), copy=False)
        vh = vh.astype(result_t, copy=False)
        return SVDResult(wrap(u), s, wrap(vh))
    else:
        signature = 'D->d' if isComplexType(t) else 'd->d'
        with errstate(call=_raise_linalgerror_svd_nonconvergence,
                      invalid='call', over='ignore', divide='ignore',
                      under='ignore'):
            s = _umath_linalg.svd(a, signature=signature)
        s = s.astype(_realType(result_t), copy=False)
        return s


def svd(ctx, A, full_matrices = False, compute_uv = True, overwrite_a = False):
    """
    "svd" is a unified interface for "svd_r" and "svd_c". Depending on
    whether A is real or complex the appropriate function is called.

    This routine computes the singular value decomposition of a matrix A.
    Given A, two orthogonal (A real) or unitary (A complex) matrices U and V
    are calculated such that

           A = U S V        and        U' U = 1         and         V V' = 1

    where S is a suitable shaped matrix whose off-diagonal elements are zero.
    Here ' denotes the hermitian transpose (i.e. transposition and complex
    conjugation). The diagonal elements of S are the singular values of A,
    i.e. the squareroots of the eigenvalues of A' A or A A'.

    input:
      A             : a real or complex matrix of shape (m, n)
      full_matrices : if true, U and V are of shape (m, m) and (n, n).
                      if false, U and V are of shape (m, min(m, n)) and (min(m, n), n).
      compute_uv    : if true, U and V are calculated. if false, only S is calculated.
      overwrite_a   : if true, allows modification of A which may improve
                      performance. if false, A is not modified.

    output:
      U : an orthogonal or unitary matrix: U' U = 1. if full_matrices is true, U is of
          shape (m, m). ortherwise it is of shape (m, min(m, n)).

      S : an array of length min(m, n) containing the singular values of A sorted by
          decreasing magnitude.

      V : an orthogonal or unitary matrix: V V' = 1. if full_matrices is true, V is of
          shape (n, n). ortherwise it is of shape (min(m, n), n).

    return value:

           S          if compute_uv is false
       (U, S, V)      if compute_uv is true

    overview of the matrices:

      full_matrices true:
        A           : m*n
        U           : m*m     U' U  = 1
        S as matrix : m*n
        V           : n*n     V  V' = 1

     full_matrices false:
        A           : m*n
        U           : m*min(n,m)             U' U  = 1
        S as matrix : min(m,n)*min(m,n)
        V           : min(m,n)*n             V  V' = 1

    examples:

       >>> from mpmath import mp
       >>> A = mp.matrix([[2, -2, -1], [3, 4, -2], [-2, -2, 0]])
       >>> S = mp.svd(A, compute_uv = False)
       >>> print(S)
       [6.0]
       [3.0]
       [1.0]

       >>> U, S, V = mp.svd(A)
       >>> print(mp.chop(A - U * mp.diag(S) * V))
       [0.0  0.0  0.0]
       [0.0  0.0  0.0]
       [0.0  0.0  0.0]

    see also: svd_r, svd_c
    """

    iscomplex = any(type(x) is ctx.mpc for x in A)

    if iscomplex:
        return ctx.svd_c(A, full_matrices = full_matrices, compute_uv = compute_uv, overwrite_a = overwrite_a)
    else:
        return ctx.svd_r(A, full_matrices = full_matrices, compute_uv = compute_uv, overwrite_a = overwrite_a)


def svd(
    x: ArrayLike,
    *,
    full_matrices: bool = True,
    compute_uv: Literal[True],
    subset_by_index: tuple[int, int] | None = None,
    algorithm: SvdAlgorithm | None = None,
) -> tuple[Array, Array, Array]:
  ...


def svd(
    x: ArrayLike,
    *,
    full_matrices: bool = True,
    compute_uv: Literal[False],
    subset_by_index: tuple[int, int] | None = None,
    algorithm: SvdAlgorithm | None = None,
) -> Array:
  ...


def svd(
    x: ArrayLike,
    *,
    full_matrices: bool = True,
    compute_uv: bool = True,
    subset_by_index: tuple[int, int] | None = None,
    algorithm: SvdAlgorithm | None = None,
) -> Array | tuple[Array, Array, Array]:
  ...


def svd(
    x: ArrayLike,
    *,
    full_matrices: bool = True,
    compute_uv: bool = True,
    subset_by_index: tuple[int, int] | None = None,
    algorithm: SvdAlgorithm | None = None,
) -> Array | tuple[Array, Array, Array]:
  """Singular value decomposition.

  Computes the singular value decomposition of an input matrix.

  Args:
    x: A batch of matrices with shape ``[..., m, n]``.
    full_matrices: Determines if full or reduced matrices are returned.
    compute_uv: If ``True``, returns the left singular vectors, the singular
      values and the adjoint of the right singular vectors. Otherwise, only
      the singular values are returned.
    subset_by_index: If ``None``, the entire matrix is returned. Otherwise,
      returns the singular values and vectors for the given range of indices.
    algorithm: The SVD algorithm to use. Must be ``None`` or a value from
      :class:`~jax.lax.linalg.SvdAlgorithm`.

  Returns:
    The singular values if ``compute_uv`` is ``False``, otherwise returns a
    triple containing the left singular vectors, the singular values, and the
    adjoint of the right singular vectors.
  """
  result = svd_p.bind(
      x,
      full_matrices=full_matrices,
      compute_uv=compute_uv,
      subset_by_index=subset_by_index,
      algorithm=algorithm,
  )
  if compute_uv:
    s, u, v = result
    return u, s, v
  else:
    s, = result
    return s


def svd(
    a: ArrayLike,
    full_matrices: bool = True,
    *,
    compute_uv: Literal[True],
    hermitian: bool = False,
    subset_by_index: tuple[int, int] | None = None,
) -> SVDResult:
  ...


def svd(
    a: ArrayLike,
    full_matrices: bool,
    compute_uv: Literal[True],
    hermitian: bool = False,
    subset_by_index: tuple[int, int] | None = None,
) -> SVDResult:
  ...


def svd(
    a: ArrayLike,
    full_matrices: bool = True,
    *,
    compute_uv: Literal[False],
    hermitian: bool = False,
    subset_by_index: tuple[int, int] | None = None,
) -> Array:
  ...


def svd(
    a: ArrayLike,
    full_matrices: bool,
    compute_uv: Literal[False],
    hermitian: bool = False,
    subset_by_index: tuple[int, int] | None = None,
) -> Array:
  ...


def svd(
    a: ArrayLike,
    full_matrices: bool = True,
    compute_uv: bool = True,
    hermitian: bool = False,
    subset_by_index: tuple[int, int] | None = None,
) -> Array | SVDResult:
  ...


def svd(
    a: ArrayLike,
    full_matrices: bool = True,
    compute_uv: bool = True,
    hermitian: bool = False,
    subset_by_index: tuple[int, int] | None = None,
) -> Array | SVDResult:
  r"""Compute the singular value decomposition.

  JAX implementation of :func:`numpy.linalg.svd`, implemented in terms of
  :func:`jax.lax.linalg.svd`.

  The SVD of a matrix `A` is given by

  .. math::

     A = U\Sigma V^H

  - :math:`U` contains the left singular vectors and satisfies :math:`U^HU=I`
  - :math:`V` contains the right singular vectors and satisfies :math:`V^HV=I`
  - :math:`\Sigma` is a diagonal matrix of singular values.

  Args:
    a: input array, of shape ``(..., N, M)``
    full_matrices: if True (default) compute the full matrices; i.e. ``u`` and ``vh`` have
      shape ``(..., N, N)`` and ``(..., M, M)``. If False, then the shapes are
      ``(..., N, K)`` and ``(..., K, M)`` with ``K = min(N, M)``.
    compute_uv: if True (default), return the full SVD ``(u, s, vh)``. If False then return
      only the singular values ``s``.
    hermitian: if True, assume the matrix is hermitian, which allows for a more efficient
      implementation (default=False)
    subset_by_index: (TPU-only) Optional 2-tuple [start, end] indicating the range of
      indices of singular values to compute. For example, if ``[n-2, n]`` then
      ``svd`` computes the two largest singular values and their singular vectors.
      Only compatible with ``full_matrices=False``.

  Returns:
    A tuple of arrays ``(u, s, vh)`` if ``compute_uv`` is True, otherwise the array ``s``.

    - ``u``: left singular vectors of shape ``(..., N, N)`` if ``full_matrices`` is True
      or ``(..., N, K)`` otherwise.
    - ``s``: singular values of shape ``(..., K)``
    - ``vh``: conjugate-transposed right singular vectors of shape ``(..., M, M)``
      if ``full_matrices`` is True or ``(..., K, M)`` otherwise.

    where ``K = min(N, M)``.

  See also:
    - :func:`jax.scipy.linalg.svd`: SciPy-style SVD API
    - :func:`jax.lax.linalg.svd`: XLA-style SVD API

  Examples:
    Consider the SVD of a small real-valued array:

    >>> x = jnp.array([[1., 2., 3.],
    ...                [6., 5., 4.]])
    >>> u, s, vt = jnp.linalg.svd(x, full_matrices=False)
    >>> s  # doctest: +SKIP
    Array([9.361919 , 1.8315067], dtype=float32)

    The singular vectors are in the columns of ``u`` and ``v = vt.T``. These vectors are
    orthonormal, which can be demonstrated by comparing the matrix product with the
    identity matrix:

    >>> jnp.allclose(u.T @ u, jnp.eye(2), atol=1E-5)
    Array(True, dtype=bool)
    >>> v = vt.T
    >>> jnp.allclose(v.T @ v, jnp.eye(2), atol=1E-5)
    Array(True, dtype=bool)

    Given the SVD, ``x`` can be reconstructed via matrix multiplication:

    >>> x_reconstructed = u @ jnp.diag(s) @ vt
    >>> jnp.allclose(x_reconstructed, x)
    Array(True, dtype=bool)
  """
  a = ensure_arraylike("jnp.linalg.svd", a)
  a, = promote_dtypes_inexact(a)
  if hermitian:
    w, v = lax_linalg.eigh(a, subset_by_index=subset_by_index)
    s = lax.abs(v)
    if compute_uv:
      sign = lax.sign(v)
      idx_dtype = lax_utils.int_dtype_for_dim(
          s.shape[s.ndim - 1], signed=False)
      idxs = lax.broadcasted_iota(idx_dtype, s.shape, dimension=s.ndim - 1)
      s, idxs, sign = lax.sort((s, idxs, sign), dimension=-1, num_keys=1)
      s = lax.rev(s, dimensions=[s.ndim - 1])
      idxs = lax.rev(idxs, dimensions=[s.ndim - 1])
      sign = lax.rev(sign, dimensions=[s.ndim - 1])
      u = indexing.take_along_axis(w, idxs[..., None, :], axis=-1)
      vh = _H(u * sign[..., None, :].astype(u.dtype))
      return SVDResult(u, s, vh)
    else:
      return lax.rev(lax.sort(s, dimension=-1), dimensions=[s.ndim-1])

  if compute_uv:
    u, s, vh = lax_linalg.svd(
        a,
        full_matrices=full_matrices,
        compute_uv=True,
        subset_by_index=subset_by_index,
    )
    return SVDResult(u, s, vh)
  else:
    return lax_linalg.svd(
        a,
        full_matrices=full_matrices,
        compute_uv=False,
        subset_by_index=subset_by_index,
    )


def svd(a: ArrayLike, full_matrices: bool = True, compute_uv: Literal[True] = True,
        overwrite_a: bool = False, check_finite: bool = True,
        lapack_driver: str = 'gesdd') -> tuple[Array, Array, Array]: ...


def svd(a: ArrayLike, full_matrices: bool, compute_uv: Literal[False],
        overwrite_a: bool = False, check_finite: bool = True,
        lapack_driver: str = 'gesdd') -> Array: ...


def svd(a: ArrayLike, full_matrices: bool = True, *, compute_uv: Literal[False],
        overwrite_a: bool = False, check_finite: bool = True,
        lapack_driver: str = 'gesdd') -> Array: ...


def svd(a: ArrayLike, full_matrices: bool = True, compute_uv: bool = True,
        overwrite_a: bool = False, check_finite: bool = True,
        lapack_driver: str = 'gesdd') -> Array | tuple[Array, Array, Array]: ...


def svd(a: ArrayLike, full_matrices: bool = True, compute_uv: bool = True,
        overwrite_a: bool = False, check_finite: bool = True,
        lapack_driver: str = 'gesdd') -> Array | tuple[Array, Array, Array]:
  r"""Compute the singular value decomposition.

  JAX implementation of :func:`scipy.linalg.svd`.

  The SVD of a matrix `A` is given by

  .. math::

     A = U\Sigma V^H

  - :math:`U` contains the left singular vectors and satisfies :math:`U^HU=I`
  - :math:`V` contains the right singular vectors and satisfies :math:`V^HV=I`
  - :math:`\Sigma` is a diagonal matrix of singular values.

  Args:
    a: input array, of shape ``(..., N, M)``
    full_matrices: if True (default) compute the full matrices; i.e. ``u`` and ``vh`` have
      shape ``(..., N, N)`` and ``(..., M, M)``. If False, then the shapes are
      ``(..., N, K)`` and ``(..., K, M)`` with ``K = min(N, M)``.
    compute_uv: if True (default), return the full SVD ``(u, s, vh)``. If False then return
      only the singular values ``s``.
    overwrite_a: unused by JAX
    check_finite: unused by JAX
    lapack_driver: unused by JAX. If you want to select a non-default SVD driver, please
      check :func:`jax.lax.linalg.svd` which provides such functionality.

  Returns:
    A tuple of arrays ``(u, s, vh)`` if ``compute_uv`` is True, otherwise the array ``s``.

    - ``u``: left singular vectors of shape ``(..., N, N)`` if ``full_matrices`` is True
      or ``(..., N, K)`` otherwise.
    - ``s``: singular values of shape ``(..., K)``
    - ``vh``: conjugate-transposed right singular vectors of shape ``(..., M, M)``
      if ``full_matrices`` is True or ``(..., K, M)`` otherwise.

    where ``K = min(N, M)``.

  See also:
    - :func:`jax.numpy.linalg.svd`: NumPy-style SVD API
    - :func:`jax.lax.linalg.svd`: XLA-style SVD API

  Examples:
    Consider the SVD of a small real-valued array:

    >>> x = jnp.array([[1., 2., 3.],
    ...                [6., 5., 4.]])
    >>> u, s, vt = jax.scipy.linalg.svd(x, full_matrices=False)
    >>> s  # doctest: +SKIP
    Array([9.361919 , 1.8315067], dtype=float32)

    The singular vectors are in the columns of ``u`` and ``v = vt.T``. These vectors are
    orthonormal, which can be demonstrated by comparing the matrix product with the
    identity matrix:

    >>> jnp.allclose(u.T @ u, jnp.eye(2), atol=1E-5)
    Array(True, dtype=bool)
    >>> v = vt.T
    >>> jnp.allclose(v.T @ v, jnp.eye(2), atol=1E-5)
    Array(True, dtype=bool)

    Given the SVD, ``x`` can be reconstructed via matrix multiplication:

    >>> x_reconstructed = u @ jnp.diag(s) @ vt
    >>> jnp.allclose(x_reconstructed, x)
    Array(True, dtype=bool)
  """
  del overwrite_a, check_finite, lapack_driver  # unused
  return _svd(a, full_matrices=full_matrices, compute_uv=compute_uv)


def svd(
    a: Any,
    full_matrices: bool,
    compute_uv: bool = True,
    hermitian: bool = False,
    max_iterations: int = 10,
    subset_by_index: tuple[int, int] | None = None,
) -> Any | Sequence[Any]:
  """Singular value decomposition.

  Args:
    a: A matrix of shape `m x n`.
    full_matrices: If True, `u` and `vh` have the shapes `m x m` and `n x n`,
      respectively. If False, the shapes are `m x k` and `k x n`, respectively,
      where `k = min(m, n)`.
    compute_uv: Whether to also compute `u` and `v` in addition to `s`.
    hermitian: True if `a` is Hermitian.
    max_iterations: The predefined maximum number of iterations of QDWH.
    subset_by_index: Optional 2-tuple [start, end] indicating the range of
      indices of singular components to compute. For example, if
      ``subset_by_index`` = [0,2], then ``svd`` computes the two largest
      singular values (and their singular vectors if `compute_uv` is true.

  Returns:
    A 3-tuple (`u`, `s`, `vh`), where `u` and `vh` are unitary matrices,
    `s` is vector of length `k` containing the singular values in the
    non-increasing order, and `k = min(m, n)`. The shapes of `u` and `vh`
    depend on the value of `full_matrices`. For `compute_uv=False`,
    only `s` is returned.
  """
  full_matrices = core.concrete_or_error(
      bool, full_matrices, 'The `full_matrices` argument must be statically '
      'specified to use `svd` within JAX transformations.')

  compute_uv = core.concrete_or_error(
      bool, compute_uv, 'The `compute_uv` argument must be statically '
      'specified to use `svd` within JAX transformations.')

  hermitian = core.concrete_or_error(
      bool,
      hermitian,
      'The `hermitian` argument must be statically '
      'specified to use `svd` within JAX transformations.',
  )

  max_iterations = core.concrete_or_error(
      int,
      max_iterations,
      'The `max_iterations` argument must be statically '
      'specified to use `svd` within JAX transformations.',
  )

  if subset_by_index is not None:
    if len(subset_by_index) != 2:
      raise ValueError('subset_by_index must be a tuple of size 2.')
    # Make sure subset_by_index is a concrete tuple.
    subset_by_index = (
        operator.index(subset_by_index[0]),
        operator.index(subset_by_index[1]),
    )
    if subset_by_index[0] >= subset_by_index[1]:
      raise ValueError('Got empty index range in subset_by_index.')
    if subset_by_index[0] < 0:
      raise ValueError('Indices in subset_by_index must be non-negative.')
    m, n = a.shape
    rank = n if n < m else m
    if subset_by_index[1] > rank:
      raise ValueError('Index in subset_by_index[1] exceeds matrix size.')
    if full_matrices and subset_by_index != (0, rank):
      raise ValueError(
          'full_matrices and subset_by_index cannot be both be set.'
      )
    # By convention, eigenvalues are numbered in non-decreasing order, while
    # singular values are numbered non-increasing order, so change
    # subset_by_index accordingly.
    subset_by_index = (rank - subset_by_index[1], rank - subset_by_index[0])

  m, n = a.shape
  is_flip = False
  if m < n:
    a = a.T.conj()
    m, n = a.shape
    is_flip = True

  u_out_null: Array | None
  q: Array | None

  if full_matrices and m > n:
    q_full, a_full = lax_linalg.qr(a, pivoting=False, full_matrices=True)
    q = q_full[:, :n]
    u_out_null = q_full[:, n:]
    a = a_full[:n, :]
  elif m > 1.15 * n:
    # The constant `1.15` comes from Yuji Nakatsukasa's implementation
    # https://www.mathworks.com/matlabcentral/fileexchange/36830-symmetric-eigenvalue-decomposition-and-the-svd?s_tid=FX_rc3_behav
    q, a = lax_linalg.qr(a, pivoting=False, full_matrices=False)
    u_out_null = None
  else:
    q = None
    u_out_null = None

  if not compute_uv:
    with config.default_matmul_precision('float32'):
      return _svd_tall_and_square_input(
          a, hermitian, compute_uv, max_iterations, subset_by_index
      )

  with config.default_matmul_precision('float32'):
    u_out, s_out, v_out = _svd_tall_and_square_input(
        a, hermitian, compute_uv, max_iterations, subset_by_index
    )
    if q is not None:  # (full_matrices and m > n) or (m > 1.15 * n)
      u_out = q @ u_out

  if u_out_null is not None:  # full_matrices and m > n
    u_out = jnp.hstack((u_out, u_out_null))

  is_finite = jnp.all(jnp.isfinite(a))
  cond_f = lambda args: jnp.logical_not(args[0])
  body_f = lambda args: (
      jnp.array(True),
      jnp.full_like(u_out, np.nan),
      jnp.full_like(s_out, np.nan),
      jnp.full_like(v_out, np.nan),
  )
  _, u_out, s_out, v_out = lax.while_loop(
      cond_f, body_f, (is_finite, u_out, s_out, v_out)
  )

  if is_flip:
    return (v_out, s_out, u_out.T.conj())

  return (u_out, s_out, v_out.T.conj())

