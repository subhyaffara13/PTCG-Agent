
def slogdet(a: ArrayLike):
    a = _atleast_float_1(a)
    return torch.linalg.slogdet(a)


def slogdet(x: Array, /, xp: Namespace, **kwargs: object) -> SlogdetResult:
    return SlogdetResult(*xp.linalg.slogdet(x, **kwargs))


def slogdet(a):
    """
    Compute the sign and (natural) logarithm of the determinant of an array.

    If an array has a very small or very large determinant, then a call to
    `det` may overflow or underflow. This routine is more robust against such
    issues, because it computes the logarithm of the determinant rather than
    the determinant itself.

    Parameters
    ----------
    a : (..., M, M) array_like
        Input array, has to be a square 2-D array.

    Returns
    -------
    A namedtuple with the following attributes:

    sign : (...) array_like
        A number representing the sign of the determinant. For a real matrix,
        this is 1, 0, or -1. For a complex matrix, this is a complex number
        with absolute value 1 (i.e., it is on the unit circle), or else 0.
    logabsdet : (...) array_like
        The natural log of the absolute value of the determinant.

    If the determinant is zero, then `sign` will be 0 and `logabsdet`
    will be -inf. In all cases, the determinant is equal to
    ``sign * np.exp(logabsdet)``.

    See Also
    --------
    det

    Notes
    -----
    Broadcasting rules apply, see the `numpy.linalg` documentation for
    details.

    The determinant is computed via LU factorization using the LAPACK
    routine ``z/dgetrf``.

    Examples
    --------
    The determinant of a 2-D array ``[[a, b], [c, d]]`` is ``ad - bc``:

    >>> import numpy as np
    >>> a = np.array([[1, 2], [3, 4]])
    >>> (sign, logabsdet) = np.linalg.slogdet(a)
    >>> (sign, logabsdet)
    (-1, 0.69314718055994529) # may vary
    >>> sign * np.exp(logabsdet)
    -2.0

    Computing log-determinants for a stack of matrices:

    >>> a = np.array([ [[1, 2], [3, 4]], [[1, 2], [2, 1]], [[1, 3], [3, 1]] ])
    >>> a.shape
    (3, 2, 2)
    >>> sign, logabsdet = np.linalg.slogdet(a)
    >>> (sign, logabsdet)
    (array([-1., -1., -1.]), array([ 0.69314718,  1.09861229,  2.07944154]))
    >>> sign * np.exp(logabsdet)
    array([-2., -3., -8.])

    This routine succeeds where ordinary `det` does not:

    >>> np.linalg.det(np.eye(500) * 0.1)
    0.0
    >>> np.linalg.slogdet(np.eye(500) * 0.1)
    (1, -1151.2925464970228)

    """
    a = asarray(a)
    _assert_stacked_square(a)
    t, result_t = _commonType(a)
    real_t = _realType(result_t)
    signature = 'D->Dd' if isComplexType(t) else 'd->dd'
    sign, logdet = _umath_linalg.slogdet(a, signature=signature)
    sign = sign.astype(result_t, copy=False)
    logdet = logdet.astype(real_t, copy=False)
    return SlogdetResult(sign, logdet)


def slogdet(a: ArrayLike, *, method: str | None = None) -> SlogdetResult:
  """
  Compute the sign and (natural) logarithm of the determinant of an array.

  JAX implementation of :func:`numpy.linalg.slogdet`.

  Args:
    a: array of shape ``(..., M, M)`` for which to compute the sign and log determinant.
    method: the method to use for determinant computation. Options are

      - ``'lu'`` (default): use the LU decomposition.
      - ``'qr'``: use the QR decomposition.

  Returns:
    A tuple of arrays ``(sign, logabsdet)``, each of shape ``a.shape[:-2]``

    - ``sign`` is the sign of the determinant.
    - ``logabsdet`` is the natural log of the determinant's absolute value.

  See also:
    :func:`jax.numpy.linalg.det`: direct computation of determinant

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> sign, logabsdet = jnp.linalg.slogdet(a)
    >>> sign  # -1 indicates negative determinant
    Array(-1., dtype=float32)
    >>> jnp.exp(logabsdet)  # Absolute value of determinant
    Array(2., dtype=float32)
  """
  a = ensure_arraylike("jnp.linalg.slogdet", a)
  a, = promote_dtypes_inexact(a)
  a_shape = np.shape(a)
  if len(a_shape) < 2 or a_shape[-1] != a_shape[-2]:
    raise ValueError(f"Argument to slogdet() must have shape [..., n, n], got {a_shape}")
  if method is None or method == "lu":
    n = a_shape[-1]
    if n == 1 or n == 2:
      return SlogdetResult(*_slogdet_small(a))
    return SlogdetResult(*_slogdet_lu(a))
  elif method == "qr":
    return SlogdetResult(*_slogdet_qr(a))
  else:
    raise ValueError(f"Unknown slogdet method '{method}'. Supported methods "
                     "are 'lu' (`None`), and 'qr'.")

