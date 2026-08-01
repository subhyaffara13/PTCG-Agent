
def convolution_matrix(a, n, mode='full'):
    """
    Construct a convolution matrix.

    Constructs the Toeplitz matrix representing one-dimensional
    convolution [1]_.  See the notes below for details.

    Array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    a : (..., m) array_like
        The 1-D array to convolve. N-dimensional arrays are treated as a
        batch: each slice along the last axis is a 1-D array to convolve.
    n : int
        The number of columns in the resulting matrix.  It gives the length
        of the input to be convolved with `a`.  This is analogous to the
        length of `v` in ``numpy.convolve(a, v)``.
    mode : str
        This is analogous to `mode` in ``numpy.convolve(v, a, mode)``.
        It must be one of ('full', 'valid', 'same').
        See below for how `mode` determines the shape of the result.

    Returns
    -------
    A : (..., k, n) ndarray
        The convolution matrix whose row count `k` depends on `mode`::

            =======  =========================
             mode    k
            =======  =========================
            'full'   m + n -1
            'same'   max(m, n)
            'valid'  max(m, n) - min(m, n) + 1
            =======  =========================

        For batch input, each slice of shape ``(k, n)`` along the last two
        dimensions of the output corresponds with a slice of shape ``(m,)``
        along the last dimension of the input.

    See Also
    --------
    toeplitz : Toeplitz matrix

    Notes
    -----
    The code::

        A = convolution_matrix(a, n, mode)

    creates a Toeplitz matrix `A` such that ``A @ v`` is equivalent to
    using ``convolve(a, v, mode)``.  The returned array always has `n`
    columns.  The number of rows depends on the specified `mode`, as
    explained above.

    In the default 'full' mode, the entries of `A` are given by::

        A[i, j] == (a[i-j] if (0 <= (i-j) < m) else 0)

    where ``m = len(a)``.  Suppose, for example, the input array is
    ``[x, y, z]``.  The convolution matrix has the form::

        [x, 0, 0, ..., 0, 0]
        [y, x, 0, ..., 0, 0]
        [z, y, x, ..., 0, 0]
        ...
        [0, 0, 0, ..., x, 0]
        [0, 0, 0, ..., y, x]
        [0, 0, 0, ..., z, y]
        [0, 0, 0, ..., 0, z]

    In 'valid' mode, the entries of `A` are given by::

        A[i, j] == (a[i-j+m-1] if (0 <= (i-j+m-1) < m) else 0)

    This corresponds to a matrix whose rows are the subset of those from
    the 'full' case where all the coefficients in `a` are contained in the
    row.  For input ``[x, y, z]``, this array looks like::

        [z, y, x, 0, 0, ..., 0, 0, 0]
        [0, z, y, x, 0, ..., 0, 0, 0]
        [0, 0, z, y, x, ..., 0, 0, 0]
        ...
        [0, 0, 0, 0, 0, ..., x, 0, 0]
        [0, 0, 0, 0, 0, ..., y, x, 0]
        [0, 0, 0, 0, 0, ..., z, y, x]

    In the 'same' mode, the entries of `A` are given by::

        d = (m - 1) // 2
        A[i, j] == (a[i-j+d] if (0 <= (i-j+d) < m) else 0)

    The typical application of the 'same' mode is when one has a signal of
    length `n` (with `n` greater than ``len(a)``), and the desired output
    is a filtered signal that is still of length `n`.

    For input ``[x, y, z]``, this array looks like::

        [y, x, 0, 0, ..., 0, 0, 0]
        [z, y, x, 0, ..., 0, 0, 0]
        [0, z, y, x, ..., 0, 0, 0]
        [0, 0, z, y, ..., 0, 0, 0]
        ...
        [0, 0, 0, 0, ..., y, x, 0]
        [0, 0, 0, 0, ..., z, y, x]
        [0, 0, 0, 0, ..., 0, z, y]

    .. versionadded:: 1.5.0

    References
    ----------
    .. [1] "Convolution", https://en.wikipedia.org/wiki/Convolution

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.linalg import convolution_matrix
    >>> A = convolution_matrix([-1, 4, -2], 5, mode='same')
    >>> A
    array([[ 4, -1,  0,  0,  0],
           [-2,  4, -1,  0,  0],
           [ 0, -2,  4, -1,  0],
           [ 0,  0, -2,  4, -1],
           [ 0,  0,  0, -2,  4]])

    Compare multiplication by `A` with the use of `numpy.convolve`.

    >>> x = np.array([1, 2, 0, -3, 0.5])
    >>> A @ x
    array([  2. ,   6. ,  -1. , -12.5,   8. ])

    Verify that ``A @ x`` produced the same result as applying the
    convolution function.

    >>> np.convolve([-1, 4, -2], x, mode='same')
    array([  2. ,   6. ,  -1. , -12.5,   8. ])

    For comparison to the case ``mode='same'`` shown above, here are the
    matrices produced by ``mode='full'`` and ``mode='valid'`` for the
    same coefficients and size.

    >>> convolution_matrix([-1, 4, -2], 5, mode='full')
    array([[-1,  0,  0,  0,  0],
           [ 4, -1,  0,  0,  0],
           [-2,  4, -1,  0,  0],
           [ 0, -2,  4, -1,  0],
           [ 0,  0, -2,  4, -1],
           [ 0,  0,  0, -2,  4],
           [ 0,  0,  0,  0, -2]])

    >>> convolution_matrix([-1, 4, -2], 5, mode='valid')
    array([[-2,  4, -1,  0,  0],
           [ 0, -2,  4, -1,  0],
           [ 0,  0, -2,  4, -1]])
    """
    if n <= 0:
        raise ValueError('n must be a positive integer.')

    a = np.asarray(a)

    if a.size == 0:
        raise ValueError('len(a) must be at least 1.')

    if mode not in ('full', 'valid', 'same'):
        raise ValueError(
            "'mode' argument must be one of ('full', 'valid', 'same')")

    if a.ndim > 1:
        return np.apply_along_axis(lambda a: convolution_matrix(a, n, mode), -1, a)

    # create zero padded versions of the array
    az = np.pad(a, (0, n-1), 'constant')
    raz = np.pad(a[::-1], (0, n-1), 'constant')

    if mode == 'same':
        trim = min(n, len(a)) - 1
        tb = trim//2
        te = trim - tb
        col0 = az[tb:len(az)-te]
        row0 = raz[-n-tb:len(raz)-tb]
    elif mode == 'valid':
        tb = min(n, len(a)) - 1
        te = tb
        col0 = az[tb:len(az)-te]
        row0 = raz[-n-tb:len(raz)-tb]
    else:  # 'full'
        col0 = az
        row0 = raz[-n:]
    return toeplitz(col0, row0)


def convolution_matrix(a: ArrayLike, n: int, mode: str = 'full') -> Array:
  r"""Construct a convolution matrix.

  JAX implementation of :func:`scipy.linalg.convolution_matrix`.

  Builds a Toeplitz matrix :math:`A` such that ``A @ v`` equals
  ``jnp.convolve(a, v, mode)``. The returned array has ``n`` columns;
  the row count :math:`k` depends on ``mode``:

  - ``'full'``: :math:`k = m + n - 1`
  - ``'same'``: :math:`k = \max(m, n)`
  - ``'valid'``: :math:`k = \max(m, n) - \min(m, n) + 1`

  where :math:`m` is the size of ``a`` along the last axis.

  Args:
    a: array of shape ``(..., m)`` to convolve. Must have ``m >= 1``.
    n: number of columns in the output. Must be a positive integer.
    mode: one of ``'full'``, ``'same'``, ``'valid'``. Defaults to ``'full'``.

  Returns:
    A convolution matrix of shape ``(..., k, n)``, where ``k`` depends on
    ``mode`` as described above.

  See also:
    :func:`jax.scipy.linalg.toeplitz`

  Examples:
    >>> jax.scipy.linalg.convolution_matrix(jnp.array([-1, 4, -2]), 5, mode='same')
    Array([[ 4, -1,  0,  0,  0],
           [-2,  4, -1,  0,  0],
           [ 0, -2,  4, -1,  0],
           [ 0,  0, -2,  4, -1],
           [ 0,  0,  0, -2,  4]], dtype=int32)
  """
  n = operator.index(n)
  if n <= 0:
    raise ValueError(f"n must be a positive integer; got {n}.")
  check_arraylike("convolution_matrix", a)
  a_arr = jnp.asarray(a)
  if a_arr.ndim == 0:
    raise ValueError(
        "convolution_matrix: a must be at least 1-dimensional, got a scalar.")
  m = a_arr.shape[-1]
  if m < 1:
    raise ValueError(f"len(a) must be at least 1; got shape {a_arr.shape}.")
  if mode not in ('full', 'valid', 'same'):
    raise ValueError(
        f"mode must be one of 'full', 'valid', 'same'; got {mode!r}.")
  pad_widths = [(0, 0)] * (a_arr.ndim - 1) + [(0, n - 1)]
  az = jnp.pad(a_arr, pad_widths)
  raz = jnp.pad(jnp.flip(a_arr, axis=-1), pad_widths)
  L = m + n - 1
  if mode == 'same':
    trim = min(n, m) - 1
    tb = trim // 2
    te = trim - tb
  elif mode == 'valid':
    tb = min(n, m) - 1
    te = tb
  else:  # 'full'
    tb = 0
    te = 0
  col0 = lax.slice_in_dim(az, tb, L - te, axis=-1)
  row0 = lax.slice_in_dim(raz, L - n - tb, L - tb, axis=-1)
  return toeplitz(col0, row0)

