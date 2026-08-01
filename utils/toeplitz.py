
def toeplitz(c, r=None):
    r"""
    Construct a Toeplitz matrix.

    The Toeplitz matrix has constant diagonals, with c as its first column
    and r as its first row. If r is not given, ``r == conjugate(c)`` is
    assumed.

    The documentation is written assuming array arguments are of specified
    "core" shapes. However, array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    c : array_like
        First column of the matrix.
    r : array_like, optional
        First row of the matrix. If None, ``r = conjugate(c)`` is assumed;
        in this case, if c[0] is real, the result is a Hermitian matrix.
        r[0] is ignored; the first row of the returned matrix is
        ``[c[0], r[1:]]``.

    Returns
    -------
    A : (len(c), len(r)) ndarray
        The Toeplitz matrix. Dtype is the same as ``(c[0] + r[0]).dtype``.

    See Also
    --------
    circulant : circulant matrix
    hankel : Hankel matrix
    solve_toeplitz : Solve a Toeplitz system.

    Notes
    -----
    The behavior when `c` or `r` is a scalar, or when `c` is complex and
    `r` is None, was changed in version 0.8.0. The behavior in previous
    versions was undocumented and is no longer supported.

    Examples
    --------
    >>> from scipy.linalg import toeplitz
    >>> toeplitz([1,2,3], [1,4,5,6])
    array([[1, 4, 5, 6],
           [2, 1, 4, 5],
           [3, 2, 1, 4]])
    >>> toeplitz([1.0, 2+3j, 4-1j])
    array([[ 1.+0.j,  2.-3.j,  4.+1.j],
           [ 2.+3.j,  1.+0.j,  2.-3.j],
           [ 4.-1.j,  2.+3.j,  1.+0.j]])

    """
    c = np.atleast_1d(c)
    if r is None:
        r = c.conjugate()
    else:
        r = np.atleast_1d(r)
    return _toeplitz(c, r)


def toeplitz(c: ArrayLike, r: ArrayLike | None = None) -> Array:
  r"""Construct a Toeplitz matrix.

  JAX implementation of :func:`scipy.linalg.toeplitz`.

  A Toeplitz matrix has equal diagonals: :math:`A_{ij} = k_{i - j}`
  for :math:`0 \le i < n` and :math:`0 \le j < n`. This function
  specifies the diagonals via the first column ``c`` and the first row
  ``r``, such that for row `i` and column `j`:

  .. math::

     A_{ij} = \begin{cases}
      c_{i - j} & i \ge j \\
      r_{j - i} & i < j
     \end{cases}

  Notice this implies that :math:`r_0` is ignored.

  Args:
    c: array of shape ``(..., N)`` specifying the first column.
    r: (optional) array of shape ``(..., M)`` specifying the first row. Leading
      dimensions must be broadcast-compatible with those of ``c``. If not specified,
      ``r`` defaults to ``conj(c)``.

  Returns:
    A Toeplitz matrix of shape ``(... N, M)``.

  Examples:
    Specifying ``c`` only:

    >>> c = jnp.array([1, 2, 3])
    >>> jax.scipy.linalg.toeplitz(c)
    Array([[1, 2, 3],
           [2, 1, 2],
           [3, 2, 1]], dtype=int32)

    Specifying ``c`` and ``r``:

    >>> r = jnp.array([-1, -2, -3])
    >>> jax.scipy.linalg.toeplitz(c, r)  # Note r[0] is ignored
    Array([[ 1, -2, -3],
           [ 2,  1, -2],
           [ 3,  2,  1]], dtype=int32)

    If specifying only complex-valued ``c``, ``r`` defaults to ``c.conj()``,
    resulting in a Hermitian matrix if ``c[0].imag == 0``:

    >>> c = jnp.array([1, 2+1j, 1+2j])
    >>> M = jax.scipy.linalg.toeplitz(c)
    >>> M
    Array([[1.+0.j, 2.-1.j, 1.-2.j],
           [2.+1.j, 1.+0.j, 2.-1.j],
           [1.+2.j, 2.+1.j, 1.+0.j]], dtype=complex64)
    >>> print("M is Hermitian:", jnp.all(M == M.conj().T))
    M is Hermitian: True

    For N-dimensional ``c`` and/or ``r``, the result is a batch of Toeplitz matrices:

    >>> c = jnp.array([[1, 2, 3], [4, 5, 6]])
    >>> jax.scipy.linalg.toeplitz(c)
    Array([[[1, 2, 3],
            [2, 1, 2],
            [3, 2, 1]],
    <BLANKLINE>
           [[4, 5, 6],
            [5, 4, 5],
            [6, 5, 4]]], dtype=int32)
  """
  if r is None:
    check_arraylike("toeplitz", c)
    r = jnp.conjugate(jnp.asarray(c))
  else:
    check_arraylike("toeplitz", c, r)
  return _toeplitz(jnp.atleast_1d(jnp.asarray(c)), jnp.atleast_1d(jnp.asarray(r)))

