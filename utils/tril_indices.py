
def tril_indices(n, k=0, m=None):
    if m is None:
        m = n
    return torch.tril_indices(n, m, offset=k)


def tril_indices(
    row: int,
    col: int,
    offset: int = 0,
    *,
    dtype: torch.dtype = torch.long,
    layout: torch.layout = torch.strided,
    device: DeviceLikeType = "cpu",
    pin_memory: bool = False,
) -> TensorLikeType:
    _trilu_checks("tril_indices", row, col, dtype, layout, pin_memory)

    trapezoid_size, rectangle_size, m_first_row = _get_tril_sizes(row, col, offset)
    row_offset = max(0, -offset)

    arange_kw = partial(
        torch.arange, layout=layout, device=device, pin_memory=pin_memory
    )

    # first we do the indices for top trapezoid
    xs1 = arange_kw(0, trapezoid_size, dtype=torch.float64)
    b = m_first_row - 0.5
    row_inds1 = torch.floor(-b + torch.sqrt(b * b + 2 * xs1))
    col_inds1 = torch.floor(xs1 - (2 * m_first_row - 1 + row_inds1) * row_inds1 * 0.5)
    row_inds1 = _maybe_convert_to_dtype(row_inds1 + row_offset, dtype)
    col_inds1 = _maybe_convert_to_dtype(col_inds1, dtype)

    # then bottom rectangle
    xs2 = arange_kw(0, rectangle_size, dtype=dtype)
    row_inds2 = xs2 // col + (col - m_first_row + 1 + row_offset)
    col_inds2 = xs2 % col

    return torch.stack(
        (torch.cat((row_inds1, row_inds2)), torch.cat((col_inds1, col_inds2)))
    )


def tril_indices(n, k=0, m=None):
    """
    Return the indices for the lower-triangle of an (n, m) array.

    Parameters
    ----------
    n : int
        The row dimension of the arrays for which the returned
        indices will be valid.
    k : int, optional
        Diagonal offset (see `tril` for details).
    m : int, optional
        The column dimension of the arrays for which the returned
        arrays will be valid.
        By default `m` is taken equal to `n`.


    Returns
    -------
    inds : tuple of arrays
        The row and column indices, respectively. The row indices are sorted
        in non-decreasing order, and the corresponding column indices are
        strictly increasing for each row.

    See also
    --------
    triu_indices : similar function, for upper-triangular.
    mask_indices : generic function accepting an arbitrary mask function.
    tril, triu

    Examples
    --------
    >>> import numpy as np

    Compute two different sets of indices to access 4x4 arrays, one for the
    lower triangular part starting at the main diagonal, and one starting two
    diagonals further right:

    >>> il1 = np.tril_indices(4)
    >>> il1
    (array([0, 1, 1, 2, 2, 2, 3, 3, 3, 3]), array([0, 0, 1, 0, 1, 2, 0, 1, 2, 3]))

    Note that row indices (first array) are non-decreasing, and the corresponding
    column indices (second array) are strictly increasing for each row.
    Here is how they can be used with a sample array:

    >>> a = np.arange(16).reshape(4, 4)
    >>> a
    array([[ 0,  1,  2,  3],
           [ 4,  5,  6,  7],
           [ 8,  9, 10, 11],
           [12, 13, 14, 15]])

    Both for indexing:

    >>> a[il1]
    array([ 0,  4,  5, ..., 13, 14, 15])

    And for assigning values:

    >>> a[il1] = -1
    >>> a
    array([[-1,  1,  2,  3],
           [-1, -1,  6,  7],
           [-1, -1, -1, 11],
           [-1, -1, -1, -1]])

    These cover almost the whole array (two diagonals right of the main one):

    >>> il2 = np.tril_indices(4, 2)
    >>> a[il2] = -10
    >>> a
    array([[-10, -10, -10,   3],
           [-10, -10, -10, -10],
           [-10, -10, -10, -10],
           [-10, -10, -10, -10]])

    """
    tri_ = tri(n, m, k=k, dtype=bool)

    return tuple(broadcast_to(inds, tri_.shape)[tri_]
                 for inds in indices(tri_.shape, sparse=True))


def tril_indices(n: DimSize, k: DimSize = 0, m: DimSize | None = None) -> tuple[Array, Array]:
  """Return the indices of lower triangle of an array of size ``(n, m)``.

  JAX implementation of :func:`numpy.tril_indices`.

  Args:
    n: int. Number of rows of the array for which the indices are returned.
    k: optional, int, default=0. Specifies the sub-diagonal on and below which
      the indices of lower triangle are returned. ``k=0`` refers to main diagonal,
      ``k<0`` refers to sub-diagonal below the main diagonal and ``k>0`` refers
      to sub-diagonal above the main diagonal.
    m: optional, int. Number of columns of the array for which the indices are
      returned. If not specified, then ``m = n``.

  Returns:
    A tuple of two arrays containing the indices of the lower triangle, one along
    each axis.

  See also:
    - :func:`jax.numpy.triu_indices`: Returns the indices of upper triangle of an
      array of size ``(n, m)``.
    - :func:`jax.numpy.triu_indices_from`: Returns the indices of upper triangle
      of a given array.
    - :func:`jax.numpy.tril_indices_from`: Returns the indices of lower triangle
      of a given array.

  Examples:
    If only ``n`` is provided in input, the indices of lower triangle of an array
    of size ``(n, n)`` array are returned.

    >>> jnp.tril_indices(3)
    (Array([0, 1, 1, 2, 2, 2], dtype=int32), Array([0, 0, 1, 0, 1, 2], dtype=int32))

    If both ``n`` and ``m`` are provided in input, the indices of lower triangle
    of an ``(n, m)`` array are returned.

    >>> jnp.tril_indices(3, m=2)
    (Array([0, 1, 1, 2, 2], dtype=int32), Array([0, 0, 1, 0, 1], dtype=int32))

    If ``k = 1``, the indices on and below the first sub-diagonal above the main
    diagonal are returned.

    >>> jnp.tril_indices(3, k=1)
    (Array([0, 0, 1, 1, 1, 2, 2, 2], dtype=int32), Array([0, 1, 0, 1, 2, 0, 1, 2], dtype=int32))

    If ``k = -1``, the indices on and below the first sub-diagonal below the main
    diagonal are returned.

    >>> jnp.tril_indices(3, k=-1)
    (Array([1, 2, 2], dtype=int32), Array([0, 0, 1], dtype=int32))
  """
  n = core.concrete_dim_or_error(n, "n argument of jnp.triu_indices")
  k = core.concrete_dim_or_error(k, "k argument of jnp.triu_indices")
  m = n if m is None else core.concrete_dim_or_error(m, "m argument of jnp.triu_indices")
  i, j = nonzero(tril(array_creation.ones((n, m)), k=k), size=_triu_size(m, n, -k))
  return i, j

