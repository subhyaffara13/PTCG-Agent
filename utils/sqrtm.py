
def sqrtm(A):
    """
    Compute, if exists, the matrix square root.

    The matrix square root of ``A`` is a matrix ``X`` such that ``X @ X = A``.
    Every square matrix is not guaranteed to have a matrix square root, for
    example, the array ``[[0, 1], [0, 0]]`` does not have a square root.

    Moreover, not every real matrix has a real square root. Hence, for
    real-valued matrices the return type can be complex if, numerically, there
    is an eigenvalue on the negative real axis.

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    A : ndarray
        Input with last two dimensions are square ``(..., n, n)``.

    Returns
    -------
    sqrtm : ndarray
        Computed matrix squareroot of `A` with same size ``(..., n, n)``.

    Notes
    -----
    This function uses the Schur decomposition method to compute the matrix
    square root following [1]_ and for real matrices [2]_. Moreover, note
    that, there exist matrices that have square roots that are not polynomials
    in ``A``. For a classical example from [2]_, the matrix satisfies::

            [ a, a**2 + 1]**2     [-1,  0]
            [-1,       -a]     =  [ 0, -1]

    for any scalar ``a`` but it is not a polynomial in ``-I``. Thus, they will
    not be found by this function.

    References
    ----------
    .. [1] Edvin Deadman, Nicholas J. Higham, Rui Ralha (2013)
           "Blocked Schur Algorithms for Computing the Matrix Square Root,
           Lecture Notes in Computer Science, 7782. pp. 171-182.
           :doi:`10.1016/0024-3795(87)90118-2`
    .. [2] Nicholas J. Higham (1987) "Computing real square roots of a real
           matrix", Linear Algebra and its Applications, 88/89:405-430.
           :doi:`10.1016/0024-3795(87)90118-2`

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import sqrtm
    >>> a = np.array([[1.0, 3.0], [1.0, 4.0]])
    >>> r = sqrtm(a)
    >>> r
    array([[ 0.75592895,  1.13389342],
           [ 0.37796447,  1.88982237]])
    >>> r.dot(r)
    array([[ 1.,  3.],
           [ 1.,  4.]])

    """
    a = np.asarray(A)
    _deprecate_dtypes('sqrtm', a)
    if a.size == 1 and a.ndim < 2:
        return np.array([[np.exp(a.item())]])

    if a.ndim < 2:
        raise LinAlgError('The input array must be at least two-dimensional')
    if a.shape[-1] != a.shape[-2]:
        raise LinAlgError('Last 2 dimensions of the array must be square')

    # Empty array
    if min(*a.shape) == 0:
        dtype = sqrtm(np.eye(2, dtype=a.dtype)).dtype
        return np.empty_like(a, dtype=dtype)

    # Scalar case
    if a.shape[-2:] == (1, 1):
        return np.emath.sqrt(a)

    if not np.issubdtype(a.dtype, np.inexact):
        a = a.astype(np.float64)
    elif a.dtype == np.float16:
        a = a.astype(np.float32)
    elif a.dtype.char in 'G':
        a = a.astype(np.complex128)
    elif a.dtype.char in 'g':
        a = a.astype(np.float64)

    if a.dtype.char not in 'fdFD':
        raise TypeError("scipy.linalg.sqrtm is not supported for the data type"
                        f" {a.dtype}")

    res, isIllconditioned, isSingular, info = recursive_schur_sqrtm(a)
    if info < 0:
        raise LinAlgError(f"Internal error in scipy.linalg.sqrtm: {info}")

    if isSingular or isIllconditioned:
        if isSingular:
            msg = ("Matrix is singular. The result might be inaccurate or the"
                   " array might not have a square root.")
        else:
            msg = ("Matrix is ill-conditioned. The result might be inaccurate"
                   " or the array might not have a square root.")
        warnings.warn(msg, LinAlgWarning, stacklevel=2)

    return res


def sqrtm(A: ArrayLike, blocksize: int = 1) -> Array:
  """Compute the matrix square root

  This function is implemented using :func:`scipy.linalg.schur`, which is only
  supported on CPU.

  JAX implementation of :func:`scipy.linalg.sqrtm`.

  Args:
    A: array of shape ``(N, N)``
    blocksize: Not supported in JAX; JAX always uses ``blocksize=1``.

  Returns:
    An array of shape ``(N, N)`` containing the matrix square root of ``A``

  See Also:
    :func:`jax.scipy.linalg.expm`

  Examples:
    >>> a = jnp.array([[1., 2., 3.],
    ...                [2., 4., 2.],
    ...                [3., 2., 1.]])
    >>> sqrt_a = jax.scipy.linalg.sqrtm(a)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(sqrt_a)
    [[0.92+0.71j 0.54+0.j   0.92-0.71j]
     [0.54+0.j   1.85+0.j   0.54-0.j  ]
     [0.92-0.71j 0.54-0.j   0.92+0.71j]]

    By definition, matrix multiplication of the matrix square root with itself should
    equal the input:

    >>> jnp.allclose(a, sqrt_a @ sqrt_a)
    Array(True, dtype=bool)

  Notes:
    This function implements the complex Schur method described in [1]_.  It does not use
    recursive blocking to speed up computations as a Sylvester Equation solver is not
    yet available in JAX.

  References:
    .. [1] Björck, Å., & Hammarling, S. (1983). "A Schur method for the square root of a matrix".
           Linear algebra and its applications, 52, 127-140.
  """
  if blocksize > 1:
      raise NotImplementedError("Blocked version is not implemented yet.")
  return _sqrtm(A)

