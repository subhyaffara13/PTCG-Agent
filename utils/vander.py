
def vander(x: ArrayLike, N=None, increasing=False):
    return torch.vander(x, N, increasing)


def vander(x, N=None, increasing=False):
    """
    Generate a Vandermonde matrix.

    The columns of the output matrix are powers of the input vector. The
    order of the powers is determined by the `increasing` boolean argument.
    Specifically, when `increasing` is False, the `i`-th output column is
    the input vector raised element-wise to the power of ``N - i - 1``. Such
    a matrix with a geometric progression in each row is named for Alexandre-
    Theophile Vandermonde.

    Parameters
    ----------
    x : array_like
        1-D input array.
    N : int, optional
        Number of columns in the output.  If `N` is not specified, a square
        array is returned (``N = len(x)``).
    increasing : bool, optional
        Order of the powers of the columns.  If True, the powers increase
        from left to right, if False (the default) they are reversed.

    Returns
    -------
    out : ndarray
        Vandermonde matrix.  If `increasing` is False, the first column is
        ``x^(N-1)``, the second ``x^(N-2)`` and so forth. If `increasing` is
        True, the columns are ``x^0, x^1, ..., x^(N-1)``.

    See Also
    --------
    polynomial.polynomial.polyvander

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([1, 2, 3, 5])
    >>> N = 3
    >>> np.vander(x, N)
    array([[ 1,  1,  1],
           [ 4,  2,  1],
           [ 9,  3,  1],
           [25,  5,  1]])

    >>> np.column_stack([x**(N-1-i) for i in range(N)])
    array([[ 1,  1,  1],
           [ 4,  2,  1],
           [ 9,  3,  1],
           [25,  5,  1]])

    >>> x = np.array([1, 2, 3, 5])
    >>> np.vander(x)
    array([[  1,   1,   1,   1],
           [  8,   4,   2,   1],
           [ 27,   9,   3,   1],
           [125,  25,   5,   1]])
    >>> np.vander(x, increasing=True)
    array([[  1,   1,   1,   1],
           [  1,   2,   4,   8],
           [  1,   3,   9,  27],
           [  1,   5,  25, 125]])

    The determinant of a square Vandermonde matrix is the product
    of the differences between the values of the input vector:

    >>> np.linalg.det(np.vander(x))
    48.000000000000043 # may vary
    >>> (5-3)*(5-2)*(5-1)*(3-2)*(3-1)*(2-1)
    48

    """
    x = asarray(x)
    if x.ndim != 1:
        raise ValueError("x must be a one-dimensional array or sequence.")
    if N is None:
        N = len(x)

    v = empty((len(x), N), dtype=promote_types(x.dtype, int))
    tmp = v[:, ::-1] if not increasing else v

    if N > 0:
        tmp[:, 0] = 1
    if N > 1:
        tmp[:, 1:] = x[:, None]
        multiply.accumulate(tmp[:, 1:], out=tmp[:, 1:], axis=1)

    return v


def vander(x, n=None):
    """
    Masked values in the input array result in rows of zeros.

    """
    _vander = np.vander(x, n)
    m = getmask(x)
    if m is not nomask:
        _vander[m] = 0
    return _vander


def vander(
    x: ArrayLike, N: int | None = None, increasing: bool = False
) -> Array:
  """Generate a Vandermonde matrix.

  JAX implementation of :func:`numpy.vander`.

  Args:
    x: input array. Must have ``x.ndim == 1``.
    N: int, optional, default=None. Specifies the number of the columns the
      output matrix. If not specified, ``N = len(x)``.
    increasing: bool, optional, default=False. Specifies the order of the powers
      of the columns. If ``True``, the powers increase from left to right,
      :math:`[x^0, x^1, ..., x^{(N-1)}]`. By default, the powers decrease from left to
      right :math:`[x^{(N-1)}, ..., x^1, x^0]`.

  Returns:
    An array of shape ``[len(x), N]`` containing the generated Vandermonde matrix.

  Examples:
    >>> x = jnp.array([1, 2, 3, 4])
    >>> jnp.vander(x)
    Array([[ 1,  1,  1,  1],
           [ 8,  4,  2,  1],
           [27,  9,  3,  1],
           [64, 16,  4,  1]], dtype=int32)

    If ``N = 2``, generates a Vandermonde matrix with ``2`` columns.

    >>> jnp.vander(x, N=2)
    Array([[1, 1],
           [2, 1],
           [3, 1],
           [4, 1]], dtype=int32)

    Generates the Vandermonde matrix in increasing order of powers, when
    ``increasing=True``.

    >>> jnp.vander(x, increasing=True)
    Array([[ 1,  1,  1,  1],
           [ 1,  2,  4,  8],
           [ 1,  3,  9, 27],
           [ 1,  4, 16, 64]], dtype=int32)
  """
  x = util.ensure_arraylike("vander", x)
  if x.ndim != 1:
    raise ValueError("x must be a one-dimensional array")
  N = x.shape[0] if N is None else core.concrete_or_error(
    operator.index, N, "'N' argument of jnp.vander()")
  if N < 0:
    raise ValueError("N must be nonnegative")

  iota = lax.iota(x.dtype, N)
  if not increasing:
    iota = lax.sub(lax._const(iota, N - 1), iota)

  return ufuncs.power(x[..., None], expand_dims(iota, tuple(range(x.ndim))))

