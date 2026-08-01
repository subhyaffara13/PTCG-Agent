
def hankel(c, r=None):
    r"""
    Construct a Hankel matrix.

    The Hankel matrix has constant anti-diagonals, with `c` as its
    first column and `r` as its last row. If the first element of `r`
    differs from the last element of `c`, the first element of `r` is
    replaced by the last element of `c` to ensure that anti-diagonals
    remain constant. If `r` is not given, then `r = zeros_like(c)` is
    assumed.

    Parameters
    ----------
    c : array_like
        First column of the matrix.
    r : array_like, optional
        Last row of the matrix. If None, ``r = zeros_like(c)`` is assumed.
        r[0] is ignored; the last row of the returned matrix is
        ``[c[-1], r[1:]]``.

        .. warning::

            Beginning in SciPy 1.19, multidimensional input will be treated as a batch,
            not ``ravel``\ ed. To preserve the existing behavior, ``ravel`` arguments
            before passing them to `toeplitz`.

    Returns
    -------
    A : (len(c), len(r)) ndarray
        The Hankel matrix. Dtype is the same as ``(c[0] + r[0]).dtype``.

    See Also
    --------
    toeplitz : Toeplitz matrix
    circulant : circulant matrix

    Examples
    --------
    >>> from scipy.linalg import hankel
    >>> hankel([1, 17, 99])
    array([[ 1, 17, 99],
           [17, 99,  0],
           [99,  0,  0]])
    >>> hankel([1,2,3,4], [4,7,7,8,9])
    array([[1, 2, 3, 4, 7],
           [2, 3, 4, 7, 7],
           [3, 4, 7, 7, 8],
           [4, 7, 7, 8, 9]])

    """
    c = np.asarray(c)
    if r is None:
        r = np.zeros_like(c)
    else:
        r = np.asarray(r)

    if c.ndim > 1 or r.ndim > 1:
        msg = ("Beginning in SciPy 1.19, multidimensional input will be treated as a "
               "batch, not `ravel`ed. To preserve the existing behavior and silence "
               "this warning, `ravel` arguments before passing them to `hankel`.")
        warnings.warn(msg, FutureWarning, stacklevel=2)
        c, r = c.ravel(), r.ravel()

    # Form a 1-D array of values to be used in the matrix, containing `c`
    # followed by r[1:].
    vals = np.concatenate((c, r[1:]))
    # Stride on concatenated array to get hankel matrix
    out_shp = len(c), len(r)
    n = vals.strides[0]
    return as_strided(vals, shape=out_shp, strides=(n, n)).copy()


def hankel(c: ArrayLike, r: ArrayLike | None = None) -> Array:
  r"""Construct a Hankel matrix.

  JAX implementation of :func:`scipy.linalg.hankel`.

  A Hankel matrix has constant anti-diagonals: ``H[i, j] = v[i + j]``, where
  ``v = concatenate([c, r[1:]])``. Notice this implies that ``r[0]`` is ignored.

  Args:
    c: array of shape ``(..., N)`` specifying the first column.
    r: (optional) array of shape ``(..., M)`` specifying the last row. Leading
      dimensions must be broadcast-compatible with those of ``c``. If not
      specified, ``r`` defaults to ``zeros_like(c)``.

  Returns:
    A Hankel matrix of shape ``(..., N, M)``.

  Examples:
    >>> c = jnp.array([1, 2, 3])
    >>> jax.scipy.linalg.hankel(c)
    Array([[1, 2, 3],
           [2, 3, 0],
           [3, 0, 0]], dtype=int32)

    >>> r = jnp.array([999, 4, 5, 6]) # Note r[0] is ignored
    >>> jax.scipy.linalg.hankel(c, r)
    Array([[1, 2, 3, 4],
           [2, 3, 4, 5],
           [3, 4, 5, 6]], dtype=int32)

    For N-dimensional ``c`` and/or ``r``, the result is a batch of Hankel matrices.
  """
  if r is None:
    check_arraylike("hankel", c)
    c = jnp.asarray(c)
    r = jnp.zeros_like(c)
  else:
    check_arraylike("hankel", c, r)
    c = jnp.asarray(c)
    r = jnp.asarray(r)
  if c.ndim == 0:
    raise ValueError("hankel: c must be at least 1-dimensional, got a scalar.")
  if r.ndim == 0:
    raise ValueError("hankel: r must be at least 1-dimensional, got a scalar.")

  # Align batch ranks so jnp.vectorize doesn't need implicit rank promotion.
  if c.ndim < r.ndim:
    c = lax.expand_dims(c, range(r.ndim - c.ndim))
  elif r.ndim < c.ndim:
    r = lax.expand_dims(r, range(c.ndim - r.ndim))

  return _hankel(c, r)

