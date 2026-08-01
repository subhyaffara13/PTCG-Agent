
def qr(a: ArrayLike, mode="reduced"):
    a = _atleast_float_1(a)
    result = torch.linalg.qr(a, mode=mode)
    if mode == "r":
        # match NumPy
        result = result.R
    return result


def qr(expr):
    return QofQR(expr), RofQR(expr)


def qr(a, overwrite_a=False, lwork=_NoValue, mode="full", pivoting=False,
    check_finite=True):
    """
    Compute QR decomposition of a matrix.

    Calculate the decomposition ``A = Q R`` where Q is unitary/orthogonal
    and R upper triangular.

    Parameters
    ----------
    a : (..., M, N) array_like
        Matrix to be decomposed
    overwrite_a : bool, optional
        Whether to overwrite data in `a` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    lwork : int, optional
        Work array size, lwork >= a.shape[1]. If None or -1, an optimal size
        is computed.

        .. deprecated:: 1.18.0
            This keyword is deprecated as well as no longer in use and will be
            removed in 1.20.0.

    mode : {'full', 'r', 'economic', 'raw'}, optional
        Determines what information is to be returned: either both Q and R
        ('full', default), only R ('r') or both Q and R but computed in
        economy-size ('economic', see Notes). The final option 'raw'
        (added in SciPy 0.11) makes the function return two matrices
        (Q, TAU) in the internal format used by LAPACK.
    pivoting : bool, optional
        Whether or not factorization should include pivoting for rank-revealing
        qr decomposition. If pivoting, compute the decomposition
        ``A[..., :, P] = Q @ R`` as above, but where P is chosen such that the
        diagonal of R is non-increasing. Equivalently, albeit less efficiently,
        an explicit P matrix may be formed explicitly by permuting the rows or columns
        (depending on the side of the equation on which it is to be used) of
        an identity matrix. See Examples.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.

    Returns
    -------
    Q : float or complex ndarray
        Of shape (..., M, M), or (..., M, K) for ``mode='economic'``. Not returned
        if ``mode='r'``. Replaced by tuple ``(Q, TAU)`` if ``mode='raw'``.
    R : float or complex ndarray
        Of shape (..., M, N), or (..., K, N) for ``mode in ['economic', 'raw']``.
        ``K = min(M, N)``.
    P : int ndarray
        Of shape (..., N,) for ``pivoting=True``. Not returned if
        ``pivoting=False``.

    Raises
    ------
    LinAlgError
        Raised if decomposition fails

    Notes
    -----
    This is an interface to the LAPACK routines dgeqrf, zgeqrf,
    dorgqr, zungqr, dgeqp3, and zgeqp3.

    If ``mode=economic``, the shapes of Q and R are (..., M, K) and (..., K, N) instead
    of (..., M,M) and (..., M,N), with ``K=min(M,N)``.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import linalg
    >>> rng = np.random.default_rng()
    >>> a = rng.standard_normal((9, 6))

    >>> q, r = linalg.qr(a)
    >>> np.allclose(a, np.dot(q, r))
    True
    >>> q.shape, r.shape
    ((9, 9), (9, 6))

    >>> r2 = linalg.qr(a, mode='r')
    >>> np.allclose(r, r2)
    True

    >>> q3, r3 = linalg.qr(a, mode='economic')
    >>> q3.shape, r3.shape
    ((9, 6), (6, 6))

    >>> q4, r4, p4 = linalg.qr(a, pivoting=True)
    >>> d = np.abs(np.diag(r4))
    >>> np.all(d[1:] <= d[:-1])
    True
    >>> np.allclose(a[:, p4], np.dot(q4, r4))
    True
    >>> P = np.eye(p4.size)[p4]
    >>> np.allclose(a, np.dot(q4, r4) @ P)
    True
    >>> np.allclose(a @ P.T, np.dot(q4, r4))
    True
    >>> q4.shape, r4.shape, p4.shape
    ((9, 9), (9, 6), (6,))

    >>> q5, r5, p5 = linalg.qr(a, mode='economic', pivoting=True)
    >>> q5.shape, r5.shape, p5.shape
    ((9, 6), (6, 6), (6,))
    >>> P = np.eye(6)[:, p5]
    >>> np.allclose(a @ P, np.dot(q5, r5))
    True
    """
    # structure mappings, keep in sync with the C side
    modes = {
        "full": 1,
        "qr": 1, # equivalent to `full`
        "r": 11,
        "raw": 21,
        "economic": 31
    }

    # 'qr' was the old default, equivalent to 'full'. Neither 'full' nor
    # 'qr' are used below.
    # 'raw' is used internally by qr_multiply
    if mode not in modes.keys():
        raise ValueError(f"Mode argument should be one of {list(modes.keys())}")

    modeFlag = modes[mode] # convert the string to an int for the C enum

    if check_finite:
        a1 = np.asarray_chkfinite(a)
    else:
        a1 = np.asarray(a)

    _deprecate_dtypes("linalg.qr", a1)

    if a1.ndim < 2:
        raise ValueError("Expected at least a 2-D array")

    M, N = a1.shape[-2], a1.shape[-1]

    # Throw error for backwards compat, else raise DeprecationWarning
    if lwork is not _NoValue:
        if lwork is not None and lwork != -1 and lwork <= M:
            raise ValueError(f"lwork should be None, -1 or > M, got {lwork}")

        else:
            warnings.warn(
                "scipy.linalg: the `lwork` keyword is deprecated and no longer in use"
                " as of SciPy 1.18.0 and will be removed in SciPy 1.20.0",
                DeprecationWarning,
                stacklevel=2
            )

    # First normalize dtypes to ensure consistent return types
    a1, overwrite_a = _normalize_lapack_dtype(a1, overwrite_a)

    # accommodate empty arrays
    if a1.size == 0:
        K = min(M, N)
        batch_shape = a1.shape[:-2]

        if mode not in ['economic', 'raw']:
            Q = np.empty_like(a1, shape=batch_shape + (M, M))
            Q[..., :, :] = np.identity(M)
            R = np.empty_like(a1)
        else:
            Q = np.empty_like(a1, shape=batch_shape + (M, K))
            R = np.empty_like(a1, shape=batch_shape + (K, N))

        if pivoting:
            Rj = R, np.arange(N, dtype=np.int64 if HAS_ILP64 else np.int32)
        else:
            Rj = R,

        if mode == 'r':
            return Rj
        elif mode == 'raw':
            qr = np.empty_like(a1, shape=batch_shape + (M, N))
            tau = np.zeros_like(a1, shape=batch_shape + (K,))
            return ((qr, tau),) + Rj

        return (Q,) + Rj

    if not (a1.flags['ALIGNED'] and a1.dtype.byteorder == '='):
        overwrite_a = True
        a1 = a1.copy()

    overwrite_a = overwrite_a or (_datacopied(a1, a))
    overwrite_a = overwrite_a and (a1.ndim == 2) and a1.flags["F_CONTIGUOUS"]

    # heavy lifting
    Q, R, tau, jpvt, err_lst = _batched_linalg._qr(a1, overwrite_a, modeFlag, pivoting)

    if err_lst:
        _format_emit_errors_warnings(err_lst)

    # construct return objects
    if pivoting:
        Rj = R, jpvt
    else:
        Rj = (R,)

    if modeFlag == modes["raw"]:
        Q = (Q, tau)
    elif modeFlag == modes["economic"] and M < N:
        Q = Q[..., :, :M]

    if modeFlag == modes["r"]:
        return Rj
    else:
        return (Q,) + Rj


def qr(A):
    m = A.shape[0]
    n = A.shape[1]

    Q = np.eye(m)
    T = A.T
    P = np.linspace(0, n-1, n, dtype=int)

    for j in range(n):
        k = np.argmax(primasum(primapow2(T[j:n+1, j:m+1]), axis=1), axis=0)
        if k > 0 and k <= n - j - 1:
            k += j
            P[j], P[k] = P[k], P[j]
            T[[j, k], :] = T[[k, j], :]
        for i in range(m-1, j, -1):
            G = planerot(T[j, [j, i]]).T
            T[j, [j, i]] = np.append(hypot(T[j, j], T[j, i]), 0)
            T[j + 1:n + 1, [j, i]] = matprod(T[j + 1:n + 1, [j, i]], G)
            Q[:, [j, i]] = matprod(Q[:, [j, i]], G)

    R = T.T

    return Q, R, P


def qr(
    x: Array,
    /,
    xp: Namespace,
    *,
    mode: Literal["reduced", "complete"] = "reduced",
    **kwargs: object,
) -> QRResult:
    return QRResult(*xp.linalg.qr(x, mode=mode, **kwargs))


def qr(  # type: ignore[no-redef]
    x: Array,
    mode: Literal["reduced", "complete"] = "reduced",
    **kwargs: object,
) -> QRResult:
    if mode != "reduced":
        raise ValueError("dask arrays only support using mode='reduced'")
    return QRResult(*da.linalg.qr(x, **kwargs))


def qr(a, mode='reduced'):
    """
    Compute the qr factorization of a matrix.

    Factor the matrix `a` as *qr*, where `q` is orthonormal and `r` is
    upper-triangular.

    Parameters
    ----------
    a : array_like, shape (..., M, N)
        An array-like object with the dimensionality of at least 2.
    mode : {'reduced', 'complete', 'r', 'raw'}, optional, default: 'reduced'
        If K = min(M, N), then

        * 'reduced'  : returns Q, R with dimensions (..., M, K), (..., K, N)
        * 'complete' : returns Q, R with dimensions (..., M, M), (..., M, N)
        * 'r'        : returns R only with dimensions (..., K, N)
        * 'raw'      : returns h, tau with dimensions (..., N, M), (..., K,)

        The options 'reduced', 'complete, and 'raw' are new in numpy 1.8,
        see the notes for more information. The default is 'reduced', and to
        maintain backward compatibility with earlier versions of numpy both
        it and the old default 'full' can be omitted. Note that array h
        returned in 'raw' mode is transposed for calling Fortran. The
        'economic' mode is deprecated.  The modes 'full' and 'economic' may
        be passed using only the first letter for backwards compatibility,
        but all others must be spelled out. See the Notes for more
        explanation.


    Returns
    -------
    Q : ndarray of float or complex, optional
        A matrix with orthonormal columns. When mode = 'complete' the
        result is an orthogonal/unitary matrix depending on whether or not
        a is real/complex. The determinant may be either +/- 1 in that
        case. In case the number of dimensions in the input array is
        greater than 2 then a stack of the matrices with above properties
        is returned.
    R : ndarray of float or complex, optional
        The upper-triangular matrix or a stack of upper-triangular
        matrices if the number of dimensions in the input array is greater
        than 2.
    (h, tau) : ndarrays of np.double or np.cdouble, optional
        The array h contains the Householder reflectors that generate q
        along with r. The tau array contains scaling factors for the
        reflectors. In the deprecated  'economic' mode only h is returned.

    Raises
    ------
    LinAlgError
        If factoring fails.

    See Also
    --------
    scipy.linalg.qr : Similar function in SciPy.
    scipy.linalg.rq : Compute RQ decomposition of a matrix.

    Notes
    -----
    When mode is 'reduced' or 'complete', the result will be a namedtuple with
    the attributes ``Q`` and ``R``.

    This is an interface to the LAPACK routines ``dgeqrf``, ``zgeqrf``,
    ``dorgqr``, and ``zungqr``.

    For more information on the qr factorization, see for example:
    https://en.wikipedia.org/wiki/QR_factorization

    Subclasses of `ndarray` are preserved except for the 'raw' mode. So if
    `a` is of type `matrix`, all the return values will be matrices too.

    New 'reduced', 'complete', and 'raw' options for mode were added in
    NumPy 1.8.0 and the old option 'full' was made an alias of 'reduced'.  In
    addition the options 'full' and 'economic' were deprecated.  Because
    'full' was the previous default and 'reduced' is the new default,
    backward compatibility can be maintained by letting `mode` default.
    The 'raw' option was added so that LAPACK routines that can multiply
    arrays by q using the Householder reflectors can be used. Note that in
    this case the returned arrays are of type np.double or np.cdouble and
    the h array is transposed to be FORTRAN compatible.  No routines using
    the 'raw' return are currently exposed by numpy, but some are available
    in lapack_lite and just await the necessary work.

    Examples
    --------
    >>> import numpy as np
    >>> rng = np.random.default_rng()
    >>> a = rng.normal(size=(9, 6))
    >>> Q, R = np.linalg.qr(a)
    >>> np.allclose(a, np.dot(Q, R))  # a does equal QR
    True
    >>> R2 = np.linalg.qr(a, mode='r')
    >>> np.allclose(R, R2)  # mode='r' returns the same R as mode='full'
    True
    >>> a = np.random.normal(size=(3, 2, 2)) # Stack of 2 x 2 matrices as input
    >>> Q, R = np.linalg.qr(a)
    >>> Q.shape
    (3, 2, 2)
    >>> R.shape
    (3, 2, 2)
    >>> np.allclose(a, np.matmul(Q, R))
    True

    Example illustrating a common use of `qr`: solving of least squares
    problems

    What are the least-squares-best `m` and `y0` in ``y = y0 + mx`` for
    the following data: {(0,1), (1,0), (1,2), (2,1)}. (Graph the points
    and you'll see that it should be y0 = 0, m = 1.)  The answer is provided
    by solving the over-determined matrix equation ``Ax = b``, where::

      A = array([[0, 1], [1, 1], [1, 1], [2, 1]])
      x = array([[y0], [m]])
      b = array([[1], [0], [2], [1]])

    If A = QR such that Q is orthonormal (which is always possible via
    Gram-Schmidt), then ``x = inv(R) * (Q.T) * b``.  (In numpy practice,
    however, we simply use `lstsq`.)

    >>> A = np.array([[0, 1], [1, 1], [1, 1], [2, 1]])
    >>> A
    array([[0, 1],
           [1, 1],
           [1, 1],
           [2, 1]])
    >>> b = np.array([1, 2, 2, 3])
    >>> Q, R = np.linalg.qr(A)
    >>> p = np.dot(Q.T, b)
    >>> np.dot(np.linalg.inv(R), p)
    array([  1.,   1.])

    """
    if mode not in ('reduced', 'complete', 'r', 'raw'):
        if mode in ('f', 'full'):
            # 2013-04-01, 1.8
            msg = (
                "The 'full' option is deprecated in favor of 'reduced'.\n"
                "For backward compatibility let mode default."
            )
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            mode = 'reduced'
        elif mode in ('e', 'economic'):
            # 2013-04-01, 1.8
            msg = "The 'economic' option is deprecated."
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            mode = 'economic'
        else:
            raise ValueError(f"Unrecognized mode '{mode}'")

    a, wrap = _makearray(a)
    _assert_stacked_2d(a)
    m, n = a.shape[-2:]
    t, result_t = _commonType(a)
    a = a.astype(t, copy=True)
    a = _to_native_byte_order(a)
    mn = min(m, n)

    signature = 'D->D' if isComplexType(t) else 'd->d'
    with errstate(call=_raise_linalgerror_qr, invalid='call',
                  over='ignore', divide='ignore', under='ignore'):
        tau = _umath_linalg.qr_r_raw(a, signature=signature)

    # handle modes that don't return q
    if mode == 'r':
        r = triu(a[..., :mn, :])
        r = r.astype(result_t, copy=False)
        return wrap(r)

    if mode == 'raw':
        q = transpose(a)
        q = q.astype(result_t, copy=False)
        tau = tau.astype(result_t, copy=False)
        return wrap(q), tau

    if mode == 'economic':
        a = a.astype(result_t, copy=False)
        return wrap(a)

    # mc is the number of columns in the resulting q
    # matrix. If the mode is complete then it is
    # same as number of rows, and if the mode is reduced,
    # then it is the minimum of number of rows and columns.
    if mode == 'complete' and m > n:
        mc = m
        gufunc = _umath_linalg.qr_complete
    else:
        mc = mn
        gufunc = _umath_linalg.qr_reduced

    signature = 'DD->D' if isComplexType(t) else 'dd->d'
    with errstate(call=_raise_linalgerror_qr, invalid='call',
                  over='ignore', divide='ignore', under='ignore'):
        q = gufunc(a, tau, signature=signature)
    r = triu(a[..., :mc, :])

    q = q.astype(result_t, copy=False)
    r = r.astype(result_t, copy=False)

    return QRResult(wrap(q), wrap(r))


def qr(x: ArrayLike, *, pivoting: Literal[False] = False, full_matrices: bool = True,
      use_magma: bool | None = None) -> tuple[Array, Array]:
  ...


def qr(x: ArrayLike, *, pivoting: Literal[True], full_matrices: bool = True,
      use_magma: bool | None = None) -> tuple[Array, Array, Array]:
  ...


def qr(x: ArrayLike, *, pivoting: bool = False, full_matrices: bool = True,
      use_magma: bool | None = None
      ) -> tuple[Array, Array] | tuple[Array, Array, Array]:
  ...


def qr(x: ArrayLike, *, pivoting: bool = False, full_matrices: bool = True,
       use_magma: bool | None = None
      ) -> tuple[Array, Array] | tuple[Array, Array, Array]:
  r"""QR decomposition.

  Computes the QR decomposition

  .. math::
    A = Q \, R

  of matrices :math:`A`, such that :math:`Q` is a unitary (orthogonal) matrix,
  and :math:`R` is an upper-triangular matrix.

  Args:
    x: A batch of matrices with shape ``[..., m, n]``.
    pivoting: Allows the QR decomposition to be rank-revealing. If ``True``,
      compute the column pivoted decomposition ``A[:, P] = Q @ R``, where ``P``
      is chosen such that the diagonal of ``R`` is non-increasing. Currently
      supported on CPU and GPU backends only.
    full_matrices: Determines if full or reduced matrices are returned; see
      below.
    use_magma: Locally override the ``jax_use_magma`` flag. If ``True``, the
      pivoted `qr` factorization is computed using MAGMA. If ``False``, the
      computation is done using LAPACK on the host CPU. If ``None`` (default),
      the behavior is controlled by the ``jax_use_magma`` flag. This argument is
      only used on GPU.

  Returns:
    A pair of arrays ``(q, r)``, if ``pivoting=False``, otherwise ``(q, r, p)``.

    Array ``q`` is a unitary (orthogonal) matrix,
    with shape ``[..., m, m]`` if ``full_matrices=True``, or
    ``[..., m, min(m, n)]`` if ``full_matrices=False``.

    Array ``r`` is an upper-triangular matrix with shape ``[..., m, n]`` if
    ``full_matrices=True``, or ``[..., min(m, n), n]`` if
    ``full_matrices=False``.

    Array ``p`` is an index vector with shape [..., n]

  Notes:
    - `MAGMA <https://icl.utk.edu/magma/>`_ support is experimental - see
      :func:`jax.lax.linalg.eig` for further assumptions and limitations.
    - If ``jax_use_magma`` is set to ``"auto"``, the MAGMA implementation will
      be used if the library can be found, and the input matrix is sufficiently
      large (has at least 2048 columns).
  """
  q, r, *p = qr_p.bind(x, pivoting=pivoting, full_matrices=full_matrices,
                       use_magma=use_magma)
  if pivoting:
    return q, r, p[0]
  return q, r


def qr(a: ArrayLike,
       mode: Literal["reduced", "complete", "raw", "full"] = "reduced",
       ) -> QRResult: ...


def qr(a: ArrayLike, mode: Literal["r"]) -> Array: ...


def qr(a: ArrayLike, mode: str) -> Array | QRResult: ...


def qr(a: ArrayLike, mode: str = "reduced") -> Array | QRResult:
  """Compute the QR decomposition of an array

  JAX implementation of :func:`numpy.linalg.qr`.

  The QR decomposition of a matrix `A` is given by

  .. math::

     A = QR

  Where `Q` is a unitary matrix (i.e. :math:`Q^HQ=I`) and `R` is an upper-triangular
  matrix.

  Args:
    a: array of shape (..., M, N)
    mode: Computational mode. Supported values are:

      - ``"reduced"`` (default): return `Q` of shape ``(..., M, K)`` and `R` of shape
        ``(..., K, N)``, where ``K = min(M, N)``.
      - ``"complete"``: return `Q` of shape ``(..., M, M)`` and `R` of shape ``(..., M, N)``.
      - ``"raw"``: return lapack-internal representations of shape ``(..., M, N)`` and ``(..., K)``.
      - ``"r"``: return `R` only.

  Returns:
    A tuple ``(Q, R)`` (if ``mode`` is not ``"r"``) otherwise an array ``R``,
    where:

    - ``Q`` is an orthogonal matrix of shape ``(..., M, K)`` (if ``mode`` is ``"reduced"``)
      or ``(..., M, M)`` (if ``mode`` is ``"complete"``).
    - ``R`` is an upper-triangular matrix of shape ``(..., M, N)`` (if ``mode`` is
      ``"r"`` or ``"complete"``) or ``(..., K, N)`` (if ``mode`` is ``"reduced"``)

    with ``K = min(M, N)``.

  See also:
    - :func:`jax.scipy.linalg.qr`: SciPy-style QR decomposition API
    - :func:`jax.lax.linalg.qr`: XLA-style QR decomposition API

  Examples:
    Compute the QR decomposition of a matrix:

    >>> a = jnp.array([[1., 2., 3., 4.],
    ...                [5., 4., 2., 1.],
    ...                [6., 3., 1., 5.]])
    >>> Q, R = jnp.linalg.qr(a)
    >>> Q  # doctest: +SKIP
    Array([[-0.12700021, -0.7581426 , -0.6396022 ],
           [-0.63500065, -0.43322435,  0.63960224],
           [-0.7620008 ,  0.48737738, -0.42640156]], dtype=float32)
    >>> R  # doctest: +SKIP
    Array([[-7.8740077, -5.080005 , -2.4130025, -4.953006 ],
           [ 0.       , -1.7870499, -2.6534991, -1.028908 ],
           [ 0.       ,  0.       , -1.0660033, -4.050814 ]], dtype=float32)

    Check that ``Q`` is orthonormal:

    >>> jnp.allclose(Q.T @ Q, jnp.eye(3), atol=1E-5)
    Array(True, dtype=bool)

    Reconstruct the input:

    >>> jnp.allclose(Q @ R, a)
    Array(True, dtype=bool)
  """
  a = ensure_arraylike("jnp.linalg.qr", a)
  a, = promote_dtypes_inexact(a)
  if mode == "raw":
    a, taus = lax_linalg.geqrf(a)
    return QRResult(a.mT, taus)
  if mode in ("reduced", "r", "full"):
    full_matrices = False
  elif mode == "complete":
    full_matrices = True
  else:
    raise ValueError(f"Unsupported QR decomposition mode '{mode}'")
  q, r = lax_linalg.qr(a, pivoting=False, full_matrices=full_matrices)
  if mode == "r":
    return r
  return QRResult(q, r)


def qr(a: ArrayLike,  overwrite_a: bool = False, lwork: Any = None, *,
       mode: Literal["full", "economic"], pivoting: Literal[False] = False,
       check_finite: bool = True) -> tuple[Array, Array]: ...


def qr(a: ArrayLike,  overwrite_a: bool = False, lwork: Any = None, *,
       mode: Literal["full", "economic"], pivoting: Literal[True] = True,
       check_finite: bool = True) -> tuple[Array, Array, Array]: ...


def qr(a: ArrayLike,  overwrite_a: bool = False, lwork: Any = None, *,
       mode: Literal["full", "economic"], pivoting: bool = False,
       check_finite: bool = True
      ) -> tuple[Array, Array] | tuple[Array, Array, Array]: ...


def qr(a: ArrayLike,  overwrite_a: bool = False, lwork: Any = None, *,
       mode: Literal["r"], pivoting: Literal[False] = False, check_finite: bool = True
      ) -> tuple[Array]: ...


def qr(a: ArrayLike,  overwrite_a: bool = False, lwork: Any = None, *,
       mode: Literal["r"], pivoting: Literal[True] = True, check_finite: bool = True
      ) -> tuple[Array, Array]: ...


def qr(a: ArrayLike,  overwrite_a: bool = False, lwork: Any = None, *,
       mode: Literal["r"], pivoting: bool = False, check_finite: bool = True
      ) -> tuple[Array] | tuple[Array, Array]: ...


def qr(a: ArrayLike, overwrite_a: bool = False, lwork: Any = None, mode: str = "full",
       pivoting: bool = False, check_finite: bool = True
      ) -> tuple[Array] | tuple[Array, Array] | tuple[Array, Array, Array]: ...


def qr(a: ArrayLike, overwrite_a: bool = False, lwork: Any = None, mode: str = "full",
       pivoting: bool = False, check_finite: bool = True
      ) -> tuple[Array] | tuple[Array, Array] | tuple[Array, Array, Array]:
  """Compute the QR decomposition of an array

  JAX implementation of :func:`scipy.linalg.qr`.

  The QR decomposition of a matrix `A` is given by

  .. math::

     A = QR

  Where `Q` is a unitary matrix (i.e. :math:`Q^HQ=I`) and `R` is an upper-triangular
  matrix.

  Args:
    a: array of shape (..., M, N)
    mode: Computational mode. Supported values are:

      - ``"full"`` (default): return `Q` of shape ``(M, M)`` and `R` of shape ``(M, N)``.
      - ``"r"``: return only `R`
      - ``"economic"``: return `Q` of shape ``(M, K)`` and `R` of shape ``(K, N)``,
        where K = min(M, N).

    pivoting: Allows the QR decomposition to be rank-revealing. If ``True``, compute
      the column-pivoted decomposition ``A[:, P] = Q @ R``, where ``P`` is chosen such
      that the diagonal of ``R`` is non-increasing.
    overwrite_a: unused in JAX
    lwork: unused in JAX
    check_finite: unused in JAX

  Returns:
    A tuple ``(Q, R)`` or ``(Q, R, P)``, if ``mode`` is not ``"r"`` and ``pivoting`` is
    respectively ``False`` or ``True``, otherwise an array ``R`` or tuple ``(R, P)`` if
    mode is ``"r"``, and ``pivoting`` is respectively ``False`` or ``True``, where:

    - ``Q`` is an orthogonal matrix of shape ``(..., M, M)`` (if ``mode`` is ``"full"``)
      or ``(..., M, K)`` (if ``mode`` is ``"economic"``),
    - ``R`` is an upper-triangular matrix of shape ``(..., M, N)`` (if ``mode`` is
      ``"r"`` or ``"full"``) or ``(..., K, N)`` (if ``mode`` is ``"economic"``),
    - ``P`` is an index vector of shape ``(..., N)``.

    with ``K = min(M, N)``.

  Notes:
    - At present, pivoting is only implemented on the CPU and GPU backends. For further
      details about the GPU implementation, see the documentation for
      :func:`jax.lax.linalg.qr`.

  See also:
    - :func:`jax.numpy.linalg.qr`: NumPy-style QR decomposition API
    - :func:`jax.lax.linalg.qr`: XLA-style QR decomposition API

  Examples:
    Compute the QR decomposition of a matrix:

    >>> a = jnp.array([[1., 2., 3., 4.],
    ...                [5., 4., 2., 1.],
    ...                [6., 3., 1., 5.]])
    >>> Q, R = jax.scipy.linalg.qr(a)
    >>> Q  # doctest: +SKIP
    Array([[-0.12700021, -0.7581426 , -0.6396022 ],
           [-0.63500065, -0.43322435,  0.63960224],
           [-0.7620008 ,  0.48737738, -0.42640156]], dtype=float32)
    >>> R  # doctest: +SKIP
    Array([[-7.8740077, -5.080005 , -2.4130025, -4.953006 ],
           [ 0.       , -1.7870499, -2.6534991, -1.028908 ],
           [ 0.       ,  0.       , -1.0660033, -4.050814 ]], dtype=float32)

    Check that ``Q`` is orthonormal:

    >>> jnp.allclose(Q.T @ Q, jnp.eye(3), atol=1E-5)
    Array(True, dtype=bool)

    Reconstruct the input:

    >>> jnp.allclose(Q @ R, a)
    Array(True, dtype=bool)
  """
  del overwrite_a, lwork, check_finite  # unused
  return _qr(a, mode, pivoting)

