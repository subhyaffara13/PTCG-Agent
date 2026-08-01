
def invhilbert(n, exact=False):
    """
    Compute the inverse of the Hilbert matrix of order `n`.

    The entries in the inverse of a Hilbert matrix are integers. When `n`
    is greater than 14, some entries in the inverse exceed the upper limit
    of 64 bit integers. The `exact` argument provides two options for
    dealing with these large integers.

    Parameters
    ----------
    n : int
        The order of the Hilbert matrix.
    exact : bool, optional
        If False, the data type of the array that is returned is np.float64,
        and the array is an approximation of the inverse.
        If True, the array is the exact integer inverse array. To represent
        the exact inverse when n > 14, the returned array is an object array
        of long integers. For n <= 14, the exact inverse is returned as an
        array with data type np.int64.

    Returns
    -------
    invh : (n, n) ndarray
        The data type of the array is np.float64 if `exact` is False.
        If `exact` is True, the data type is either np.int64 (for n <= 14)
        or object (for n > 14). In the latter case, the objects in the
        array will be long integers.

    See Also
    --------
    hilbert : Create a Hilbert matrix.

    Notes
    -----
    .. versionadded:: 0.10.0

    Examples
    --------
    >>> from scipy.linalg import invhilbert
    >>> invhilbert(4)
    array([[   16.,  -120.,   240.,  -140.],
           [ -120.,  1200., -2700.,  1680.],
           [  240., -2700.,  6480., -4200.],
           [ -140.,  1680., -4200.,  2800.]])
    >>> invhilbert(4, exact=True)
    array([[   16,  -120,   240,  -140],
           [ -120,  1200, -2700,  1680],
           [  240, -2700,  6480, -4200],
           [ -140,  1680, -4200,  2800]], dtype=int64)
    >>> invhilbert(16)[7,7]
    4.2475099528537506e+19
    >>> invhilbert(16, exact=True)[7,7]
    42475099528537378560

    """
    from scipy.special import comb
    if exact:
        if n > 14:
            dtype = object
        else:
            dtype = np.int64
    else:
        dtype = np.float64
    invh = np.empty((n, n), dtype=dtype)
    for i in range(n):
        for j in range(0, i + 1):
            s = i + j
            invh[i, j] = ((-1) ** s * (s + 1) *
                          comb(n + i, n - j - 1, exact=exact) *
                          comb(n + j, n - i - 1, exact=exact) *
                          comb(s, i, exact=exact) ** 2)
            if i != j:
                invh[j, i] = invh[i, j]
    return invh


def invhilbert(n: int) -> Array:
  r"""Compute the inverse of the Hilbert matrix of order n.

  JAX implementation of :func:`scipy.linalg.invhilbert`.

  The entries are given by a closed-form expression in terms of binomial
  coefficients:

  .. math::

     H^{-1}_{ij} = (-1)^{i + j} (i + j + 1)
                   \binom{n + i}{n - j - 1}
                   \binom{n + j}{n - i - 1}
                   \binom{i + j}{i}^2

  for :math:`0 \le i, j < n`.

  Args:
    n: the size of the matrix to create.

  Returns:
    The inverse of the Hilbert matrix of shape ``(n, n)``.

  Note:
    Unlike :func:`scipy.linalg.invhilbert`, this function does not support
    ``exact=True``. The result is computed in floating point using
    :func:`~jax.scipy.special.comb`; for large ``n`` the entries quickly
    exceed the dynamic range of finite-precision floats.

  See Also:
    :func:`jax.scipy.linalg.hilbert`

  Examples:
    >>> with jnp.printoptions(precision=3, suppress=True):
    ...   print(jax.scipy.linalg.invhilbert(2))
    ...   print(jax.scipy.linalg.invhilbert(3))
    [[ 4. -6.]
     [-6. 12.]]
    [[   9.  -36.   30.]
     [ -36.  192. -180.]
     [  30. -180.  180.]]
  """
  a = jnp.arange(n, dtype=dtypes.default_float_dtype())
  i = a[:, None]
  j = a[None, :]
  s = i + j
  return ((-1.0) ** s * (s + 1.0)
          * comb(n + i, n - j - 1)
          * comb(n + j, n - i - 1)
          * comb(s, i) ** 2)

