
def inv(a: ArrayLike):
    a = _atleast_float_1(a)
    result = torch.linalg.inv(a)
    return result


def inv(a, overwrite_a=False, check_finite=True, *, assume_a=None, lower=False):
    r"""
    Compute the inverse of a matrix.

    If the data matrix is known to be a particular type then supplying the
    corresponding string to ``assume_a`` key chooses the dedicated solver.
    The available options are

    =============================  ================================
     general                        'general' (or 'gen')
     diagonal                       'diagonal'
     upper triangular               'upper triangular'
     lower triangular               'lower triangular'
     symmetric positive definite    'pos'
     symmetric                      'sym'
     Hermitian                      'her'
    =============================  ================================

    For the 'pos' option, only the triangle of the input matrix specified in
    the `lower` argument is used, and the other triangle is not referenced.
    Likewise, an explicit `assume_a='diagonal'` means that off-diagonal elements
    are not referenced.

    The `a` array argument may have additional "batch" dimensions prepended to the core
    shape. In this case, the array is treated as a batch of lower-dimensional slices;
    see :ref:`linalg_batch` for details.

    Parameters
    ----------
    a : array_like, shape (..., M, M)
        Square matrix (or a batch of matrices) to be inverted.
    overwrite_a : bool, optional
        Discard data in `a` (may improve performance). Default is False.
        See :ref:`tutorial_linalg_overwrite` for details.
    check_finite : bool, optional
        Whether to check that the input matrix contains only finite numbers.
        Disabling may give a performance gain, but may result in problems
        (crashes, non-termination) if the inputs do contain infinities or NaNs.
    assume_a : str, optional
        Valid entries are described above.
        If omitted or ``None``, checks are performed to identify structure so the
        appropriate solver can be called.
    lower : bool, optional
        Ignored unless `assume_a` is one of 'sym', 'her', or 'pos'. If True, the
        calculation uses only the data in the lower triangle of `a`; entries above the
        diagonal are ignored. If False (default), the calculation uses only the data in
        the upper triangle of `a`; entries below the diagonal are ignored.

    Returns
    -------
    ainv : ndarray
        Inverse of the matrix `a`.

    Raises
    ------
    LinAlgError
        If `a` is singular.
    ValueError
        If `a` is not square, or not 2D.

    Notes
    -----

    This routine checks the condition number of the `a` matrix and emits a
    `LinAlgWarning` for ill-conditioned inputs.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import linalg
    >>> a = np.array([[1., 2.], [3., 4.]])
    >>> linalg.inv(a)
    array([[-2. ,  1. ],
           [ 1.5, -0.5]])
    >>> a @ linalg.inv(a)
    array([[ 1.,  0.],
           [ 0.,  1.]])

    The input array ``a`` may represent a single matrix or a collection (a.k.a.
    a "batch") of square matrices. For example, if ``a.shape == (4, 3, 2, 2)``, it is
    interpreted as a ``(4, 3)``-shaped batch of :math:`2\times 2` matrices.
    See :ref:`linalg_batch` for further details.
    To illustrate:

    >>> a = np.stack((np.eye(2), [[1, 2], [3, 4]]))
    >>> linalg.inv(a)
    array([[[ 1. ,  0. ],
            [ 0. ,  1. ]],
           [[-2. ,  1. ],
            [ 1.5, -0.5]]])

    Note that the structure detection runs per-slice: in the example above, each of the
    two slices will be independently discovered as being diagonal. Setting an explicit
    ``assume_a`` argument will bypass structure detection and use the provided value
    without checking:

    >>> a = np.stack((np.eye(2), [[1, 2], [3, 4]]))
    >>> linalg.inv(a, assume_a="diagonal")
    array([[[1.  , 0.  ],
            [0.  , 1.  ]],
           [[1.  , 2.  ],   # off-diagonal elements are incorrect
            [3.  , 0.25]]])
    """
    a1 = _asarray_validated(a, check_finite=check_finite)
    _deprecate_dtypes("linalg.inv", a1)

    if a1.ndim < 2:
        raise ValueError(f"Expected at least ndim=2, got {a1.ndim=}")
    if a1.shape[-1] != a1.shape[-2]:
        raise ValueError(f"Expected square matrix, got {a1.shape=}")

    # accommodate empty matrices
    if a1.size == 0:
        dt = inv(np.eye(2, dtype=a1.dtype)).dtype
        return np.empty_like(a1, dtype=dt)

    # Also check if dtype is LAPACK compatible
    a1, overwrite_a = _normalize_lapack_dtype(a1, overwrite_a)
    a1, overwrite_a = _ensure_aligned_and_native(a1, overwrite_a)

    # XXX can relax a1.ndim == 2?
    overwrite_a = overwrite_a and (a1.ndim == 2) and (a1.flags["F_CONTIGUOUS"])

    # keep the numbers in sync with C at `linalg/src/_common_array_utils.hh`
    structure = {
        None: -1,
        'general': 0, 'gen': 0,
        'diagonal': 11,
        'upper triangular': 21,
        'lower triangular': 22,
        'pos' : 101,
        'sym' : 201,
        'her' : 211,
    }[assume_a]

    # a1 is well behaved, invert it.
    inv_a, err_lst = _batched_linalg._inv(a1, structure, overwrite_a, lower)

    if err_lst:
        _format_emit_errors_warnings(err_lst)

    return inv_a


def inv(A):
    if not USE_NAIVE_MATH:
        return np.linalg.inv(A)
    A = A.copy()
    n = A.shape[0]
    if istril(A):
        # This case is invoked in COBYLA.
        R = A.T
        B = np.zeros((n, n))
        for i in range(n):
            B[i, i] = 1 / R[i, i]
            B[:i, i] = -matprod(B[:i, :i], R[:i, i]) / R[i, i]
        return B.T
    elif istriu(A):
        B = np.zeros((n, n))
        for i in range(n):
            B[i, i] = 1 / A[i, i]
            B[:i, i] = -matprod(B[:i, :i], A[:i, i]) / A[i, i]
    else:
        # This is NOT the best algorithm for the inverse, but since the QR subroutine is available ...
        Q, R, P = qr(A)
        R = R.T
        B = np.zeros((n, n))
        for i in range(n - 1, -1, -1):
            B[:, i] = (Q[:, i] - matprod(B[:, i + 1:n], R[i + 1:n, i])) / R[i, i]
        InvP = np.zeros(n, dtype=int)
        InvP[P] = np.linspace(0, n-1, n)
        B = B[:, InvP].T
    return B


def inv(matrix: Array) -> Array:
    xp = array_namespace(matrix)
    r_inv = xp.matrix_transpose(matrix[..., :3, :3])
    # Matrix multiplication of r_inv and translation vector
    t_inv = -(r_inv @ matrix[..., :3, 3][..., None])[..., 0]
    matrix = xp.zeros(
        (*matrix.shape[:-2], 4, 4), dtype=matrix.dtype, device=xp_device(matrix)
    )
    matrix = xpx.at(matrix)[..., :3, :3].set(r_inv)
    matrix = xpx.at(matrix)[..., :3, 3].set(t_inv)
    matrix = xpx.at(matrix)[..., 3, 3].set(1)
    return matrix


def inv(quat: Array) -> Array:
    return xpx.at(quat)[..., :3].multiply(-1, copy=True)


def inv(A):
    """
    Compute the inverse of a sparse arrays.

    Parameters
    ----------
    A : (M, M) sparse arrays
        square matrix to be inverted

    Returns
    -------
    Ainv : (M, M) sparse arrays
        inverse of `A`

    Notes
    -----
    This computes the sparse inverse of `A`. If the inverse of `A` is expected
    to be non-sparse, it will likely be faster to convert `A` to dense and use
    `scipy.linalg.inv`.

    Examples
    --------
    >>> from scipy.sparse import csc_array
    >>> from scipy.sparse.linalg import inv
    >>> A = csc_array([[1., 0.], [1., 2.]])
    >>> Ainv = inv(A)
    >>> Ainv
    <Compressed Sparse Column sparse array of dtype 'float64'
        with 3 stored elements and shape (2, 2)>
    >>> A.dot(Ainv)
    <Compressed Sparse Column sparse array of dtype 'float64'
        with 2 stored elements and shape (2, 2)>
    >>> A.dot(Ainv).toarray()
    array([[ 1.,  0.],
           [ 0.,  1.]])

    .. versionadded:: 0.12.0

    """
    # Check input
    if not (issparse(A) or is_pydata_spmatrix(A)):
        raise TypeError('Input must be a sparse arrays')

    # Use sparse direct solver to solve "AX = I" accurately
    I = _ident_like(A)
    Ainv = spsolve(A, I)
    return Ainv


def inv(a):
    """
    Compute the inverse of a matrix.

    Given a square matrix `a`, return the matrix `ainv` satisfying
    ``a @ ainv = ainv @ a = eye(a.shape[0])``.

    Parameters
    ----------
    a : (..., M, M) array_like
        Matrix to be inverted.

    Returns
    -------
    ainv : (..., M, M) ndarray or matrix
        Inverse of the matrix `a`.

    Raises
    ------
    LinAlgError
        If `a` is not square or inversion fails.

    See Also
    --------
    scipy.linalg.inv : Similar function in SciPy.
    numpy.linalg.cond : Compute the condition number of a matrix.
    numpy.linalg.svd : Compute the singular value decomposition of a matrix.

    Notes
    -----
    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    If `a` is detected to be singular, a `LinAlgError` is raised. If `a` is
    ill-conditioned, a `LinAlgError` may or may not be raised, and results may
    be inaccurate due to floating-point errors.

    References
    ----------
    .. [1] Wikipedia, "Condition number",
           https://en.wikipedia.org/wiki/Condition_number

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.linalg import inv
    >>> a = np.array([[1., 2.], [3., 4.]])
    >>> ainv = inv(a)
    >>> np.allclose(a @ ainv, np.eye(2))
    True
    >>> np.allclose(ainv @ a, np.eye(2))
    True

    If a is a matrix object, then the return value is a matrix as well:

    >>> ainv = inv(np.matrix(a))
    >>> ainv
    matrix([[-2. ,  1. ],
            [ 1.5, -0.5]])

    Inverses of several matrices can be computed at once:

    >>> a = np.array([[[1., 2.], [3., 4.]], [[1, 3], [3, 5]]])
    >>> inv(a)
    array([[[-2.  ,  1.  ],
            [ 1.5 , -0.5 ]],
           [[-1.25,  0.75],
            [ 0.75, -0.25]]])

    If a matrix is close to singular, the computed inverse may not satisfy
    ``a @ ainv = ainv @ a = eye(a.shape[0])`` even if a `LinAlgError`
    is not raised:

    >>> a = np.array([[2,4,6],[2,0,2],[6,8,14]])
    >>> inv(a)  # No errors raised
    array([[-1.12589991e+15, -5.62949953e+14,  5.62949953e+14],
       [-1.12589991e+15, -5.62949953e+14,  5.62949953e+14],
       [ 1.12589991e+15,  5.62949953e+14, -5.62949953e+14]])
    >>> a @ inv(a)
    array([[ 0.   , -0.5  ,  0.   ],  # may vary
           [-0.5  ,  0.625,  0.25 ],
           [ 0.   ,  0.   ,  1.   ]])

    To detect ill-conditioned matrices, you can use `numpy.linalg.cond` to
    compute its *condition number* [1]_. The larger the condition number, the
    more ill-conditioned the matrix is. As a rule of thumb, if the condition
    number ``cond(a) = 10**k``, then you may lose up to ``k`` digits of
    accuracy on top of what would be lost to the numerical method due to loss
    of precision from arithmetic methods.

    >>> from numpy.linalg import cond
    >>> cond(a)
    np.float64(8.659885634118668e+17)  # may vary

    It is also possible to detect ill-conditioning by inspecting the matrix's
    singular values directly. The ratio between the largest and the smallest
    singular value is the condition number:

    >>> from numpy.linalg import svd
    >>> sigma = svd(a, compute_uv=False)  # Do not compute singular vectors
    >>> sigma.max()/sigma.min()
    8.659885634118668e+17  # may vary

    """
    a, wrap = _makearray(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)

    signature = 'D->D' if isComplexType(t) else 'd->d'
    with errstate(call=_raise_linalgerror_singular, invalid='call',
                  over='ignore', divide='ignore', under='ignore'):
        ainv = _umath_linalg.inv(a, signature=signature)
    return wrap(ainv.astype(result_t, copy=False))


def inv(a: ArrayLike) -> Array:
  """Return the inverse of a square matrix

  JAX implementation of :func:`numpy.linalg.inv`.

  Args:
    a: array of shape ``(..., N, N)`` specifying square array(s) to be inverted.

  Returns:
    Array of shape ``(..., N, N)`` containing the inverse of the input.

  Notes:
    In most cases, explicitly computing the inverse of a matrix is ill-advised. For
    example, to compute ``x = inv(A) @ b``, it is more performant and numerically
    precise to use a direct solve, such as :func:`jax.scipy.linalg.solve`.

  See Also:
    - :func:`jax.scipy.linalg.inv`: SciPy-style API for matrix inverse
    - :func:`jax.numpy.linalg.solve`: direct linear solver

  Examples:
    Compute the inverse of a 3x3 matrix

    >>> a = jnp.array([[1., 2., 3.],
    ...                [2., 4., 2.],
    ...                [3., 2., 1.]])
    >>> a_inv = jnp.linalg.inv(a)
    >>> a_inv  # doctest: +SKIP
    Array([[ 0.        , -0.25      ,  0.5       ],
           [-0.25      ,  0.5       , -0.25000003],
           [ 0.5       , -0.25      ,  0.        ]], dtype=float32)

    Check that multiplying with the inverse gives the identity:

    >>> jnp.allclose(a @ a_inv, jnp.eye(3), atol=1E-5)
    Array(True, dtype=bool)

    Multiply the inverse by a vector ``b``, to find a solution to ``a @ x = b``

    >>> b = jnp.array([1., 4., 2.])
    >>> a_inv @ b
    Array([ 0.  ,  1.25, -0.5 ], dtype=float32)

    Note, however, that explicitly computing the inverse in such a case can lead
    to poor performance and loss of precision as the size of the problem grows.
    Instead, you should use a direct solver like :func:`jax.numpy.linalg.solve`:

    >>> jnp.linalg.solve(a, b)
     Array([ 0.  ,  1.25, -0.5 ], dtype=float32)
  """
  arr = ensure_arraylike("jnp.linalg.inv", a)
  if arr.ndim < 2 or arr.shape[-1] != arr.shape[-2]:
    raise ValueError(
      f"Argument to inv must have shape [..., n, n], got {arr.shape}.")
  return solve(
    arr, lax.broadcast(jnp.eye(arr.shape[-1], dtype=arr.dtype), arr.shape[:-2]))


def inv(a: ArrayLike, overwrite_a: bool = False, check_finite: bool = True) -> Array:
  """Return the inverse of a square matrix

  JAX implementation of :func:`scipy.linalg.inv`.

  Args:
    a: array of shape ``(..., N, N)`` specifying square array(s) to be inverted.
    overwrite_a: unused in JAX
    check_finite: unused in JAX

  Returns:
    Array of shape ``(..., N, N)`` containing the inverse of the input.

  Notes:
    In most cases, explicitly computing the inverse of a matrix is ill-advised. For
    example, to compute ``x = inv(A) @ b``, it is more performant and numerically
    precise to use a direct solve, such as :func:`jax.scipy.linalg.solve`.

  See Also:
    - :func:`jax.numpy.linalg.inv`: NumPy-style API for matrix inverse
    - :func:`jax.scipy.linalg.solve`: direct linear solver

  Examples:
    Compute the inverse of a 3x3 matrix

    >>> a = jnp.array([[1., 2., 3.],
    ...                [2., 4., 2.],
    ...                [3., 2., 1.]])
    >>> a_inv = jax.scipy.linalg.inv(a)
    >>> a_inv  # doctest: +SKIP
    Array([[ 0.        , -0.25      ,  0.5       ],
           [-0.25      ,  0.5       , -0.25000003],
           [ 0.5       , -0.25      ,  0.        ]], dtype=float32)

    Check that multiplying with the inverse gives the identity:

    >>> jnp.allclose(a @ a_inv, jnp.eye(3), atol=1E-5)
    Array(True, dtype=bool)

    Multiply the inverse by a vector ``b``, to find a solution to ``a @ x = b``

    >>> b = jnp.array([1., 4., 2.])
    >>> a_inv @ b
    Array([ 0.  ,  1.25, -0.5 ], dtype=float32)

    Note, however, that explicitly computing the inverse in such a case can lead
    to poor performance and loss of precision as the size of the problem grows.
    Instead, you should use a direct solver like :func:`jax.scipy.linalg.solve`:

    >>> jax.scipy.linalg.solve(a, b)
     Array([ 0.  ,  1.25, -0.5 ], dtype=float32)
  """
  del overwrite_a, check_finite  # unused
  return jnp_linalg.inv(a)


def inv(x: FloatArray['*d']) -> FloatArray['*d']:
  """Like `np.linalg.inv` but auto-support jnp, tnp, np."""
  return _tf_or_xnp(x).linalg.inv(x)

