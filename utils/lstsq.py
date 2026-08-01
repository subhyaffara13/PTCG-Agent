
def lstsq(input: Tensor, A: Tensor, *, out=None) -> tuple[Tensor, Tensor]:
    raise RuntimeError(
        "This function was deprecated since version 1.9 and is now removed. "
        "`torch.lstsq` is deprecated in favor of `torch.linalg.lstsq`.\n"
        "`torch.linalg.lstsq` has reversed arguments and does not return the QR decomposition in "
        "the returned tuple (although it returns other information about the problem).\n\n"
        "To get the QR decomposition consider using `torch.linalg.qr`.\n\n"
        "The returned solution in `torch.lstsq` stored the residuals of the solution in the "
        "last m - n columns of the returned value whenever m > n. In torch.linalg.lstsq, "
        "the residuals are in the field 'residuals' of the returned named tuple.\n\n"
        "The unpacking of the solution, as in\n"
        "X, _ = torch.lstsq(B, A).solution[:A.size(1)]\n"
        "should be replaced with:\n"
        "X = torch.linalg.lstsq(A, B).solution"
    )


def lstsq(a: ArrayLike, b: ArrayLike, rcond=None):
    a, b = _atleast_float_2(a, b)
    # NumPy is using gelsd: https://github.com/numpy/numpy/blob/v1.24.0/numpy/linalg/umath_linalg.cpp#L3991
    # on CUDA, only `gels` is available though, so use it instead
    driver = "gels" if a.is_cuda or b.is_cuda else "gelsd"
    return torch.linalg.lstsq(a, b, rcond=rcond, driver=driver)


def lstsq(a, b, cond=None, overwrite_a=False, overwrite_b=False,
          check_finite=True, lapack_driver=None):
    """
    Compute least-squares solution to the equation ``a @ x = b``.

    Compute a vector x such that the 2-norm ``|b - A x|`` is minimized.

    Parameters
    ----------
    a : (..., M, N) array_like
        Left-hand side array
    b : (M,) or (..., M, K) array_like
        Right hand side array
    cond : float, optional
        Cutoff for 'small' singular values; used to determine effective
        rank of a. Singular values smaller than
        ``cond * largest_singular_value`` are considered zero.
    overwrite_a : bool, optional
        Whether to overwrite data in `a` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    overwrite_b : bool, optional
        Whether to overwrite data in `b` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrices contain only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    lapack_driver : str, optional
        Which LAPACK driver is used to solve the least-squares problem.
        Options are ``'gelsd'``, ``'gelsy'``, ``'gelss'``. Default
        (``'gelsd'``) is a good choice.  However, ``'gelsy'`` can be slightly
        faster on many problems.  ``'gelss'`` was used historically.  It is
        generally slow but uses less memory.

        .. versionadded:: 0.17.0

    Returns
    -------
    x : (N,) or (..., N, K) ndarray
        Least-squares solution.
    residues : (K,) ndarray or float
        If `lapack_driver` is ``'gelss'`` or ``'gelsd'`` this contains the square of
        the 2-norm for each column in ``b - a x`` if ``M > N`` and ``rank == N``. If
        the rank condition is violated, ``NaN`` is returned instead. If `lapack_driver`
        if ``'gelsy'`` or ``M <= N`` a (0,)-shaped array is returned.
    rank : int
        Effective rank of `a`.
    s : (min(M, N),) ndarray or None
        Singular values of `a`. The condition number of ``a`` is
        ``s[0] / s[-1]``.

    Raises
    ------
    LinAlgError
        If computation does not converge.

    ValueError
        When parameters are not compatible.

    See Also
    --------
    scipy.optimize.nnls : linear least squares with non-negativity constraint

    Notes
    -----
    When ``'gelsy'`` is used as a driver, `s` is always ``None``.

    Array arguments of this function, `a` and `b`, may have additional "batch"
    dimensions prepended to the core shape. In this case, the array is treated as a
    batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import lstsq
    >>> import matplotlib.pyplot as plt

    Suppose we have the following data:

    >>> x = np.array([1, 2.5, 3.5, 4, 5, 7, 8.5])
    >>> y = np.array([0.3, 1.1, 1.5, 2.0, 3.2, 6.6, 8.6])

    We want to fit a quadratic polynomial of the form ``y = a + b*x**2``
    to this data.  We first form the "design matrix" M, with a constant
    column of 1s and a column containing ``x**2``:

    >>> M = x[:, np.newaxis]**[0, 2]
    >>> M
    array([[  1.  ,   1.  ],
           [  1.  ,   6.25],
           [  1.  ,  12.25],
           [  1.  ,  16.  ],
           [  1.  ,  25.  ],
           [  1.  ,  49.  ],
           [  1.  ,  72.25]])

    We want to find the least-squares solution to ``M.dot(p) = y``,
    where ``p`` is a vector with length 2 that holds the parameters
    ``a`` and ``b``.

    >>> p, res, rnk, s = lstsq(M, y)
    >>> p
    array([ 0.20925829,  0.12013861])

    Plot the data and the fitted curve.

    >>> plt.plot(x, y, 'o', label='data')
    >>> xx = np.linspace(0, 9, 101)
    >>> yy = p[0] + p[1]*xx**2
    >>> plt.plot(xx, yy, label='least squares fit, $y = a + bx^2$')
    >>> plt.xlabel('x')
    >>> plt.ylabel('y')
    >>> plt.legend(framealpha=1, shadow=True)
    >>> plt.grid(alpha=0.25)
    >>> plt.show()

    As an illustration of the "batching" feature (see :ref:`linalg_batch` for details),
    suppose that we want to compare least-squares fits of the given data with two
    models: a quadratic model above, and one with an additional linear term,
    ``y = a + b*x**2 + c*x``.
    To this end, we construct the design matrix for ``y = a + b*x**2 + c*x``, and
    extend ``M`` to have three columns:

    >>> M1 = np.hstack((M, np.zeros((7, 1))))
    >>> M2 = x[:, np.newaxis] ** [0, 2, 1]
    >>> MM = np.stack((M1, M2))
    >>> x, res, rnk, s = lstsq(MM, y)
    >>> x
    array([[0.20925829, 0.12013861, 0.        ],
           [0.0578403 , 0.11262261, 0.07701453]])
    >>> rnk
    array([2, 3])

    Note that the rows of the ``x`` solution are equivalent to using ``M1`` and ``M2``,
    respectively.
    In a similar vein, to simulate an effect of random noise on ``y``, you can turn
    it into an array with multiple columns, where each column corresponds to a specific
    realization of the noise.
    """

    driver = lapack_driver
    if driver is None:
        driver = lstsq.default_lapack_driver
    if driver not in ('gelsd', 'gelsy', 'gelss'):
        raise ValueError(f'LAPACK driver "{driver}" is not found')

    if len(a.shape) < 2:
        raise ValueError('Input array a should be at least 2D, got {a.shape = }')

    a1 = np.atleast_2d(_asarray_validated(a, check_finite=check_finite))
    b1 = np.atleast_1d(_asarray_validated(b, check_finite=check_finite))
    _deprecate_dtypes("linalg.lstsq", a1, b1)

    a1, b1 = _ensure_dtype_cdsz(a1, b1)   # NB: makes a1.dtype == b1.dtype, if needed
    a1, overwrite_a = _normalize_lapack_dtype(a1, overwrite_a)

    a1, overwrite_a = _ensure_aligned_and_native(a1, overwrite_a)
    b1, overwrite_b = _ensure_aligned_and_native(b1, overwrite_b)

    m, n = a1.shape[-2:]

    # Zero-sized problem, confuses LAPACK; bail out straight away
    if m == 0 or n == 0:
        x = np.zeros((n,) + b1.shape[1:], dtype=np.common_type(a1, b1))
        if n == 0:
            residues = np.linalg.norm(b1, axis=0)**2
        else:
            residues = np.empty((0,))
        return x, residues, 0, np.empty((0,))

    # align the shape of b with a
    # 1. make b1 at least 2D
    b_is_1D = b1.ndim == 1
    if b_is_1D:
        b1 = b1[:, None]

    if m != b1.shape[-2]:
        raise ValueError('Shape mismatch: a and b should have the same number'
                         f' of rows ({m} != {b1.shape[-2]}).')

    # 2. broadcast the batch dimensions of b1 and a1
    batch_shape = np.broadcast_shapes(a1.shape[:-2], b1.shape[:-2])
    a1 = np.broadcast_to(a1, batch_shape + a1.shape[-2:])
    b1 = np.broadcast_to(b1, batch_shape + b1.shape[-2:])

    overwrite_a = overwrite_a and (a1.ndim == 2) and a1.flags["F_CONTIGUOUS"]
    overwrite_b = (
        overwrite_b and (b1.ndim == 2) and b1.flags["F_CONTIGUOUS"] and m >= n
    ) # Only overwrite when overdetermined system, otherwise ldb will be > m

    if cond is None:
        cond = np.finfo(a1.dtype).eps
    else:
        cond = float(cond)

    x, rank, S, err_lst = _batched_linalg._lstsq(
        a1, b1, cond, driver, overwrite_a, overwrite_b
    )

    if err_lst:
        _format_emit_errors_warnings(err_lst)

    x1 = x[..., :n, :]
    if m > n and lapack_driver != "gelsy":
        residuals = np.sum(x[..., n:, :] * x[..., n:, :].conj(), axis=-2)

        # LAPACK makes no promises about residuals for non full-column rank, set to NaN
        residuals[rank < n, :] = np.nan
    else:
        residuals = np.zeros(batch_shape + (0,), dtype=x.dtype)

    if b_is_1D:
        x1 = x1[..., 0]
        if residuals.size > 0 and lapack_driver != "gelsy":
            residuals = residuals[..., 0]

    if m <= n: # residuals are empty for under- and exactly determined problems
        residuals = np.zeros(batch_shape + (0,), dtype=residuals.dtype)

    return x1, residuals, rank, S


def lstsq(a, b, rcond=None):
    r"""
    Return the least-squares solution to a linear matrix equation.

    Computes the vector `x` that approximately solves the equation
    ``a @ x = b``. The equation may be under-, well-, or over-determined
    (i.e., the number of linearly independent rows of `a` can be less than,
    equal to, or greater than its number of linearly independent columns).
    If `a` is square and of full rank, then `x` (but for round-off error)
    is the "exact" solution of the equation. Else, `x` minimizes the
    Euclidean 2-norm :math:`||b - ax||`. If there are multiple minimizing
    solutions, the one with the smallest 2-norm :math:`||x||` is returned.

    Parameters
    ----------
    a : (M, N) array_like
        "Coefficient" matrix.
    b : {(M,), (M, K)} array_like
        Ordinate or "dependent variable" values. If `b` is two-dimensional,
        the least-squares solution is calculated for each of the `K` columns
        of `b`.
    rcond : float, optional
        Cut-off ratio for small singular values of `a`.
        For the purposes of rank determination, singular values are treated
        as zero if they are smaller than `rcond` times the largest singular
        value of `a`.
        The default uses the machine precision times ``max(M, N)``.  Passing
        ``-1`` will use machine precision.

        .. versionchanged:: 2.0
            Previously, the default was ``-1``, but a warning was given that
            this would change.

    Returns
    -------
    x : {(N,), (N, K)} ndarray
        Least-squares solution. If `b` is two-dimensional,
        the solutions are in the `K` columns of `x`.
    residuals : {(1,), (K,), (0,)} ndarray
        Sums of squared residuals: Squared Euclidean 2-norm for each column in
        ``b - a @ x``.
        If the rank of `a` is < N or M <= N, this is an empty array.
        If `b` is 1-dimensional, this is a (1,) shape array.
        Otherwise the shape is (K,).
    rank : int
        Rank of matrix `a`.
    s : (min(M, N),) ndarray
        Singular values of `a`.

    Raises
    ------
    LinAlgError
        If computation does not converge.

    See Also
    --------
    scipy.linalg.lstsq : Similar function in SciPy.

    Notes
    -----
    If `b` is a matrix, then all array results are returned as matrices.

    Examples
    --------
    Fit a line, ``y = mx + c``, through some noisy data-points:

    >>> import numpy as np
    >>> x = np.array([0, 1, 2, 3])
    >>> y = np.array([-1, 0.2, 0.9, 2.1])

    By examining the coefficients, we see that the line should have a
    gradient of roughly 1 and cut the y-axis at, more or less, -1.

    We can rewrite the line equation as ``y = Ap``, where ``A = [[x 1]]``
    and ``p = [[m], [c]]``.  Now use `lstsq` to solve for `p`:

    >>> A = np.vstack([x, np.ones(len(x))]).T
    >>> A
    array([[ 0.,  1.],
           [ 1.,  1.],
           [ 2.,  1.],
           [ 3.,  1.]])

    >>> m, c = np.linalg.lstsq(A, y)[0]
    >>> m, c
    (1.0 -0.95) # may vary

    Plot the data along with the fitted line:

    >>> import matplotlib.pyplot as plt
    >>> _ = plt.plot(x, y, 'o', label='Original data', markersize=10)
    >>> _ = plt.plot(x, m*x + c, 'r', label='Fitted line')
    >>> _ = plt.legend()
    >>> plt.show()

    """
    a, _ = _makearray(a)
    b, wrap = _makearray(b)
    is_1d = b.ndim == 1
    if is_1d:
        b = b[:, newaxis]
    _assert_2d(a, b)
    m, n = a.shape[-2:]
    m2, n_rhs = b.shape[-2:]
    if m != m2:
        raise LinAlgError('Incompatible dimensions')

    t, result_t = _commonType(a, b)
    result_real_t = _realType(result_t)

    if rcond is None:
        rcond = finfo(t).eps * max(n, m)

    signature = 'DDd->Ddid' if isComplexType(t) else 'ddd->ddid'
    if n_rhs == 0:
        # lapack can't handle n_rhs = 0 - so allocate
        # the array one larger in that axis
        b = zeros(b.shape[:-2] + (m, n_rhs + 1), dtype=b.dtype)

    with errstate(call=_raise_linalgerror_lstsq, invalid='call',
                  over='ignore', divide='ignore', under='ignore'):
        x, resids, rank, s = _umath_linalg.lstsq(a, b, rcond,
                                                 signature=signature)
    if m == 0:
        x[...] = 0
    if n_rhs == 0:
        # remove the item we added
        x = x[..., :n_rhs]
        resids = resids[..., :n_rhs]

    # remove the axis we added
    if is_1d:
        x = x.squeeze(axis=-1)
        # we probably should squeeze resids too, but we can't
        # without breaking compatibility.

    # as documented
    if rank != n or m <= n:
        resids = array([], result_real_t)

    # coerce output arrays
    s = s.astype(result_real_t, copy=False)
    resids = resids.astype(result_real_t, copy=False)
    # Copying lets the memory in r_parts be freed
    x = x.astype(result_t, copy=True)
    return wrap(x), wrap(resids), rank, s


def lstsq(a: ArrayLike, b: ArrayLike, rcond: float | None = None, *,
          numpy_resid: bool = False) -> tuple[Array, Array, Array, Array]:
  """
  Return the least-squares solution to a linear equation.

  JAX implementation of :func:`numpy.linalg.lstsq`.

  Args:
    a: array of shape ``(M, N)`` representing the coefficient matrix.
    b: array of shape ``(M,)`` or ``(M, K)`` representing the right-hand side.
    rcond: Cut-off ratio for small singular values. Singular values smaller than
      ``rcond * largest_singular_value`` are treated as zero. If None (default),
      the optimal value will be used to reduce floating point errors.
    numpy_resid: If True, compute and return residuals in the same way as NumPy's
      `linalg.lstsq`. This is necessary if you want to precisely replicate NumPy's
      behavior. If False (default), a more efficient method is used to compute residuals.

  Returns:
    Tuple of arrays ``(x, resid, rank, s)`` where

    - ``x`` is a shape ``(N,)`` or ``(N, K)`` array containing the least-squares solution.
    - ``resid`` is the sum of squared residual of shape ``()`` or ``(K,)``.
    - ``rank`` is the rank of the matrix ``a``.
    - ``s`` is the singular values of the matrix ``a``.

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> b = jnp.array([5, 6])
    >>> x, _, _, _ = jnp.linalg.lstsq(a, b)
    >>> with jnp.printoptions(precision=3):
    ...   print(x)
    [-4.   4.5]
  """
  a, b = ensure_arraylike("jnp.linalg.lstsq", a, b)
  if numpy_resid:
    return _lstsq(a, b, rcond, numpy_resid=True)
  return _jit_lstsq(a, b, rcond)

