import os

def tri(
    N,
    M=None,
    k=0,
    dtype: DTypeLike | None = None,
    *,
    like: NotImplementedType = None,
):
    if M is None:
        M = N
    tensor = torch.ones((N, M), dtype=dtype)
    return torch.tril(tensor, diagonal=k)


def tri(N, M=None, k=0, dtype=float, *, like=None):
    """
    An array with ones at and below the given diagonal and zeros elsewhere.

    Parameters
    ----------
    N : int
        Number of rows in the array.
    M : int, optional
        Number of columns in the array.
        By default, `M` is taken equal to `N`.
    k : int, optional
        The sub-diagonal at and below which the array is filled.
        `k` = 0 is the main diagonal, while `k` < 0 is below it,
        and `k` > 0 is above.  The default is 0.
    dtype : dtype, optional
        Data type of the returned array.  The default is float.
    ${ARRAY_FUNCTION_LIKE}

        .. versionadded:: 1.20.0

    Returns
    -------
    tri : ndarray of shape (N, M)
        Array with its lower triangle filled with ones and zero elsewhere;
        in other words ``T[i,j] == 1`` for ``j <= i + k``, 0 otherwise.

    Examples
    --------
    >>> import numpy as np
    >>> np.tri(3, 5, 2, dtype=np.int_)
    array([[1, 1, 1, 0, 0],
           [1, 1, 1, 1, 0],
           [1, 1, 1, 1, 1]])

    >>> np.tri(3, 5, -1)
    array([[0.,  0.,  0.,  0.,  0.],
           [1.,  0.,  0.,  0.,  0.],
           [1.,  1.,  0.,  0.,  0.]])

    """

    warning_for_type = None
    try:
        N = operator.index(N)
    except TypeError:
        warning_for_type = warning_for_type or type(N)

    if like is not None:
        return _tri_with_like(like, N, M=M, k=k, dtype=dtype)

    if M is None:
        M = N
    else:
        try:
            M = operator.index(M)
        except TypeError:
            warning_for_type = warning_for_type or type(M)

    try:
        k = operator.index(k)
    except TypeError:
        warning_for_type = warning_for_type or type(k)

    m = greater_equal.outer(arange(N, dtype=_min_int(0, N)),
                            arange(-k, M - k, dtype=_min_int(-k, M - k)))

    # Avoid making a copy if the requested type is already bool
    m = m.astype(dtype, copy=False)

    # Deprecation in NumPy 2.5, 2026-03
    if warning_for_type:
        warnings.warn(
            (f"Cannot convert {(warning_for_type).__name__} safely to an integer."
             "This will raise an error in future versions (Deprecated NumPy 2.5)"),
            DeprecationWarning,
            skip_file_prefixes=(os.path.dirname(__file__),),
        )

    return m


def tri(N: int, M: int | None = None, k: int = 0, dtype: DTypeLike | None = None) -> Array:
  r"""Return an array with ones on and below the diagonal and zeros elsewhere.

  JAX implementation of :func:`numpy.tri`

  Args:
    N: int. Dimension of the rows of the returned array.
    M: optional, int. Dimension of the columns of the returned array. If not
      specified, then ``M = N``.
    k: optional, int, default=0. Specifies the sub-diagonal on and below which
      the array is filled with ones. ``k=0`` refers to main diagonal, ``k<0``
      refers to sub-diagonal below the main diagonal and ``k>0`` refers to
      sub-diagonal above the main diagonal.
    dtype: optional, data type of the returned array. The default type is float.

  Returns:
    An array of shape ``(N, M)`` containing the lower triangle with elements
    below the sub-diagonal specified by ``k`` are set to one and zero elsewhere.

  See also:
    - :func:`jax.numpy.tril`: Returns a lower triangle of an array.
    - :func:`jax.numpy.triu`: Returns an upper triangle of an array.

  Examples:
    >>> jnp.tri(3)
    Array([[1., 0., 0.],
           [1., 1., 0.],
           [1., 1., 1.]], dtype=float32)

    When ``M`` is not equal to ``N``:

    >>> jnp.tri(3, 4)
    Array([[1., 0., 0., 0.],
           [1., 1., 0., 0.],
           [1., 1., 1., 0.]], dtype=float32)

    when ``k>0``:

    >>> jnp.tri(3, k=1)
    Array([[1., 1., 0.],
           [1., 1., 1.],
           [1., 1., 1.]], dtype=float32)

    When ``k<0``:

    >>> jnp.tri(3, 4, k=-1)
    Array([[0., 0., 0., 0.],
           [1., 0., 0., 0.],
           [1., 1., 0., 0.]], dtype=float32)
  """
  if dtype is None:
    # TODO(phawkins): this is a strange default.
    dtype = np.dtype(np.float32)
  else:
    dtype = dtypes.check_and_canonicalize_user_dtype(dtype, "tri")
  M = M if M is not None else N
  return lax._tri(dtype, (N, M), k)

