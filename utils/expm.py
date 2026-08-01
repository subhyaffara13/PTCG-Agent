
def expm(A):
    """Compute the matrix exponential of an array.

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    A : ndarray
        Input with last two dimensions are square ``(..., n, n)``.

    Returns
    -------
    eA : ndarray
        The resulting matrix exponential with the same shape of ``A``

    Notes
    -----
    Implements the algorithm given in [1]_, which is essentially a Pade
    approximation with a variable order that is decided based on the array
    data.

    For input with size ``n``, the memory usage is in the worst case in the
    order of ``8*(n**2)``. If the input data is not of single and double
    precision of real and complex dtypes, it is copied to a new array.

    For cases ``n >= 400``, the exact 1-norm computation cost, breaks even with
    1-norm estimation and from that point on the estimation scheme given in
    [2]_ is used to decide on the approximation order.

    References
    ----------
    .. [1] Awad H. Al-Mohy and Nicholas J. Higham, (2009), "A New Scaling
           and Squaring Algorithm for the Matrix Exponential", SIAM J. Matrix
           Anal. Appl. 31(3):970-989, :doi:`10.1137/09074721X`

    .. [2] Nicholas J. Higham and Francoise Tisseur (2000), "A Block Algorithm
           for Matrix 1-Norm Estimation, with an Application to 1-Norm
           Pseudospectra." SIAM J. Matrix Anal. Appl. 21(4):1185-1201,
           :doi:`10.1137/S0895479899356080`

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import expm, sinm, cosm

    Matrix version of the formula exp(0) = 1:

    >>> expm(np.zeros((3, 2, 2)))
    array([[[1., 0.],
            [0., 1.]],
    <BLANKLINE>
           [[1., 0.],
            [0., 1.]],
    <BLANKLINE>
           [[1., 0.],
            [0., 1.]]])

    Euler's identity (exp(i*theta) = cos(theta) + i*sin(theta))
    applied to a matrix:

    >>> a = np.array([[1.0, 2.0], [-1.0, 3.0]])
    >>> expm(1j*a)
    array([[ 0.42645930+1.89217551j, -2.13721484-0.97811252j],
           [ 1.06860742+0.48905626j, -1.71075555+0.91406299j]])
    >>> cosm(a) + 1j*sinm(a)
    array([[ 0.42645930+1.89217551j, -2.13721484-0.97811252j],
           [ 1.06860742+0.48905626j, -1.71075555+0.91406299j]])

    """
    a = np.asarray(A)
    _deprecate_dtypes("expm", a)

    if a.size == 1 and a.ndim < 2:
        return np.array([[np.exp(a.item())]])

    if a.ndim < 2:
        raise LinAlgError('The input array must be at least two-dimensional')
    if a.shape[-1] != a.shape[-2]:
        raise LinAlgError('Last 2 dimensions of the array must be square')

    # Empty array
    if min(*a.shape) == 0:
        dtype = expm(np.eye(2, dtype=a.dtype)).dtype
        return np.empty_like(a, dtype=dtype)

    # Scalar case
    if a.shape[-2:] == (1, 1):
        return np.exp(a)

    if not np.issubdtype(a.dtype, np.inexact):
        a = a.astype(np.float64)
    elif a.dtype == np.float16:
        a = a.astype(np.float32)

    # An explicit formula for 2x2 case exists (formula (2.2) in [1]_). However, without
    # Kahan's method, numerical instabilities can occur (See gh-19584). Hence removed
    # here until we have a more stable implementation.

    eA, info = matrix_exponential(a)
    if info != 0:
        if info <= -11:
            # We raise it from failed mallocs; negative LAPACK codes > -7
            raise MemoryError("scipy.linalg.expm could not allocate "
                            "sufficient memory while trying to compute the "
                            f"exponential (error code {info}).")
        else:
            # LAPACK wrong argument error or exact singularity.
            # Neither should happen.
            raise RuntimeError("scipy.linalg.expm: Internal LAPACK "
                                "error during the exponential computation "
                                f"(error code {info})")
    return eA


def expm(A):
    """
    Compute the matrix exponential using Pade approximation.

    Parameters
    ----------
    A : (M,M) array_like or sparse array
        2D Array or Matrix (sparse or dense) to be exponentiated

    Returns
    -------
    expA : (M,M) ndarray
        Matrix exponential of `A`

    Notes
    -----
    This is algorithm (6.1) which is a simplification of algorithm (5.1).

    .. versionadded:: 0.12.0

    References
    ----------
    .. [1] Awad H. Al-Mohy and Nicholas J. Higham (2009)
           "A New Scaling and Squaring Algorithm for the Matrix Exponential."
           SIAM Journal on Matrix Analysis and Applications.
           31 (3). pp. 970-989. ISSN 1095-7162

    Examples
    --------
    >>> from scipy.sparse import csc_array
    >>> from scipy.sparse.linalg import expm
    >>> A = csc_array([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
    >>> A.toarray()
    array([[1, 0, 0],
           [0, 2, 0],
           [0, 0, 3]], dtype=int64)
    >>> Aexp = expm(A)
    >>> Aexp
    <Compressed Sparse Column sparse array of dtype 'float64'
        with 3 stored elements and shape (3, 3)>
    >>> Aexp.toarray()
    array([[  2.71828183,   0.        ,   0.        ],
           [  0.        ,   7.3890561 ,   0.        ],
           [  0.        ,   0.        ,  20.08553692]])
    """
    return _expm(A, use_exact_onenorm='auto')


def expm(A: ArrayLike, *, upper_triangular: bool = False, max_squarings: int = 16) -> Array:
  """Compute the matrix exponential

  JAX implementation of :func:`scipy.linalg.expm`.

  Args:
    A: array of shape ``(..., N, N)``
    upper_triangular: if True, then assume that ``A`` is upper-triangular. Default=False.
    max_squarings: The number of squarings in the scaling-and-squaring approximation method
     (default: 16).

  Returns:
    An array of shape ``(..., N, N)`` containing the matrix exponent of ``A``.

  Notes:
    This uses the scaling-and-squaring approximation method, with computational complexity
    controlled by the optional ``max_squarings`` argument. Theoretically, the number of
    required squarings is ``max(0, ceil(log2(norm(A))) - c)`` where ``norm(A)`` is the L1
    norm and ``c=2.42`` for float64/complex128, or ``c=1.97`` for float32/complex64.

  See Also:
    :func:`jax.scipy.linalg.expm_frechet`

  Examples:

    ``expm`` is the matrix exponential, and has similar properties to the more
    familiar scalar exponential. For scalars ``a`` and ``b``, :math:`e^{a + b}
    = e^a e^b`. However, for matrices, this property only holds when ``A`` and
    ``B`` commute (``AB = BA``). In this case, ``expm(A+B) = expm(A) @ expm(B)``

    >>> A = jnp.array([[2, 0],
    ...                [0, 1]])
    >>> B = jnp.array([[3, 0],
    ...                [0, 4]])
    >>> jnp.allclose(jax.scipy.linalg.expm(A+B),
    ...              jax.scipy.linalg.expm(A) @ jax.scipy.linalg.expm(B),
    ...              rtol=0.0001)
    Array(True, dtype=bool)

    If a matrix ``X`` is invertible, then
    ``expm(X @ A @ inv(X)) = X @ expm(A) @ inv(X)``

    >>> X = jnp.array([[3, 1],
    ...                [2, 5]])
    >>> X_inv = jax.scipy.linalg.inv(X)
    >>> jnp.allclose(jax.scipy.linalg.expm(X @ A @ X_inv),
    ...              X @ jax.scipy.linalg.expm(A) @ X_inv)
    Array(True, dtype=bool)
  """
  A, = promote_dtypes_inexact(A)

  if A.ndim < 2 or A.shape[-1] != A.shape[-2]:
    raise ValueError(f"Expected A to be a (batched) square matrix, got {A.shape=}.")

  if A.ndim > 2:
    return jnp_vectorize.vectorize(
      partial(expm, upper_triangular=upper_triangular, max_squarings=max_squarings),
      signature="(n,n)->(n,n)")(A)

  P, Q, n_squarings = _calc_P_Q(jnp.asarray(A))

  def _nan(args):
    A, *_ = args
    return jnp.full_like(A, np.nan)

  def _compute(args):
    A, P, Q = args
    R = _solve_P_Q(P, Q, upper_triangular)
    R = _squaring(R, n_squarings, max_squarings)
    return R

  R = lax.cond(n_squarings > max_squarings, _nan, _compute, (A, P, Q))
  return R

