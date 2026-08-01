
def funm(A, func, disp=True):
    """
    Evaluate a matrix function specified by a callable.

    Returns the value of matrix-valued function ``f`` at `A`. The
    function ``f`` is an extension of the scalar-valued function `func`
    to matrices.

    Parameters
    ----------
    A : (N, N) array_like
        Matrix at which to evaluate the function
    func : callable
        Callable object that evaluates a scalar function f.
        Must be vectorized (eg. using vectorize).
    disp : bool, optional
        Print warning if error in the result is estimated large
        instead of returning estimated error. (Default: True)

    Returns
    -------
    funm : (N, N) ndarray
        Value of the matrix function specified by func evaluated at `A`
    errest : float
        (if disp == False)

        1-norm of the estimated error, ||err||_1 / ||A||_1

    Notes
    -----
    This function implements the general algorithm based on Schur decomposition
    (Algorithm 9.1.1. in [1]_).

    If the input matrix is known to be diagonalizable, then relying on the
    eigendecomposition is likely to be faster. For example, if your matrix is
    Hermitian, you can do

    >>> from scipy.linalg import eigh
    >>> def funm_herm(a, func, check_finite=False):
    ...     w, v = eigh(a, check_finite=check_finite)
    ...     ## if you further know that your matrix is positive semidefinite,
    ...     ## you can optionally guard against precision errors by doing
    ...     # w = np.maximum(w, 0)
    ...     w = func(w)
    ...     return (v * w).dot(v.conj().T)

    References
    ----------
    .. [1] Gene H. Golub, Charles F. van Loan, Matrix Computations 4th ed.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import funm
    >>> a = np.array([[1.0, 3.0], [1.0, 4.0]])
    >>> funm(a, lambda x: x*x)
    array([[  4.,  15.],
           [  5.,  19.]])
    >>> a.dot(a)
    array([[  4.,  15.],
           [  5.,  19.]])

    """
    A = _asarray_square(A)
    # Perform Shur decomposition (lapack ?gees)
    T, Z = schur(A)
    T, Z = rsf2csf(T, Z)
    n, n = T.shape
    F = diag(func(diag(T)))  # apply function to diagonal elements
    F = F.astype(T.dtype.char)  # e.g., when F is real but T is complex

    minden = abs(T[0, 0])

    # implement Algorithm 11.1.1 from Golub and Van Loan
    #                 "matrix Computations."
    F, minden = _funm_loops(F, T, n, minden)

    F = dot(dot(Z, F), transpose(conjugate(Z)))
    F = _maybe_real(A, F)

    tol = {0: feps, 1: eps}[_array_precision[F.dtype.char]]
    if minden == 0.0:
        minden = tol
    err = min(1, max(tol, (tol/minden)*norm(triu(T, 1), 1)))
    if prod(ravel(logical_not(isfinite(F))), axis=0):
        err = np.inf
    if disp:
        if err > 1000*tol:
            print("funm result may be inaccurate, approximate err =", err)
        return F
    else:
        return F, err


def funm(A: ArrayLike, func: Callable[[Array], Array],
         disp: bool = True) -> Array | tuple[Array, Array]:
  """Evaluate a matrix-valued function

  JAX implementation of :func:`scipy.linalg.funm`.

  Args:
    A: array of shape ``(N, N)`` for which the function is to be computed.
    func: Callable object that takes a scalar argument and returns a scalar result.
      Represents the function to be evaluated over the eigenvalues of A.
    disp: If true (default), error information is not returned. Unlike scipy's version JAX
      does not attempt to display information at runtime.
    compute_expm: (N, N) array_like or None, optional.
      If provided, the matrix exponential of A. This is used for improving efficiency when `func`
      is the exponential function. If not provided, it is computed internally.
      Defaults to None.

  Returns:
    Array of same shape as ``A``, containing the result of ``func`` evaluated on the
    eigenvalues of ``A``.

  Notes:
    The returned dtype of JAX's implementation may differ from that of scipy;
    specifically, in cases where all imaginary parts of the array values are
    close to zero, the SciPy function may return a real-valued array, whereas
    the JAX implementation will return a complex-valued array.

  Examples:
    Applying an arbitrary matrix function:

    >>> A = jnp.array([[1., 2.], [3., 4.]])
    >>> def func(x):
    ...   return jnp.sin(x) + 2 * jnp.cos(x)
    >>> jax.scipy.linalg.funm(A, func)  # doctest: +SKIP
    Array([[ 1.2452652 +0.j, -0.3701772 +0.j],
           [-0.55526584+0.j,  0.6899995 +0.j]], dtype=complex64)

    Comparing two ways of computing the matrix exponent:

    >>> expA_1 = jax.scipy.linalg.funm(A, jnp.exp)
    >>> expA_2 = jax.scipy.linalg.expm(A)
    >>> jnp.allclose(expA_1, expA_2, rtol=1E-4)
    Array(True, dtype=bool)
  """
  A_arr = jnp.asarray(A)
  if A_arr.ndim != 2 or A_arr.shape[0] != A_arr.shape[1]:
    raise ValueError('expected square array_like input')

  T, Z = schur(A_arr)
  T, Z = rsf2csf(T, Z)

  F = jnp.diag(func(jnp.diag(T)))
  F = F.astype(T.dtype.char)

  F, minden = _algorithm_11_1_1(F, T)
  F = Z @ F @ Z.conj().T

  if disp:
    return F

  if F.dtype.char.lower() == 'e':
    tol = dtypes.finfo(np.float16).eps
  if F.dtype.char.lower() == 'f':
    tol = dtypes.finfo(np.float32).eps
  else:
    tol = dtypes.finfo(np.float64).eps

  minden = jnp.where(minden == 0.0, tol, minden)
  err = jnp.where(jnp.any(jnp.isinf(F)), np.inf, jnp.minimum(1, jnp.maximum(
          tol, (tol / minden) * norm(jnp.triu(T, 1), 1))))

  return F, err

