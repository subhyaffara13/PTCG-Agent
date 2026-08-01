
def indices(dimensions, dtype: DTypeLike | None = int, sparse=False):
    # https://github.com/numpy/numpy/blob/v1.24.0/numpy/core/numeric.py#L1691-L1791
    dimensions = tuple(dimensions)
    N = len(dimensions)
    shape = (1,) * N
    if sparse:
        res = ()
    else:
        res = torch.empty((N,) + dimensions, dtype=dtype)
    for i, dim in enumerate(dimensions):
        idx = torch.arange(dim, dtype=dtype).reshape(
            shape[:i] + (dim,) + shape[i + 1 :]
        )
        if sparse:
            res = res + (idx,)
        else:
            res[i] = idx
    return res


def indices(dimensions, dtype=int, sparse=False):
    """
    Return an array representing the indices of a grid.

    Compute an array where the subarrays contain index values 0, 1, ...
    varying only along the corresponding axis.

    Parameters
    ----------
    dimensions : sequence of ints
        The shape of the grid.
    dtype : dtype, optional
        Data type of the result.
    sparse : boolean, optional
        Return a sparse representation of the grid instead of a dense
        representation. Default is False.

    Returns
    -------
    grid : one ndarray or tuple of ndarrays
        If sparse is False:
            Returns one array of grid indices,
            ``grid.shape = (len(dimensions),) + tuple(dimensions)``.
        If sparse is True:
            Returns a tuple of arrays, with
            ``grid[i].shape = (1, ..., 1, dimensions[i], 1, ..., 1)`` with
            dimensions[i] in the ith place

    See Also
    --------
    mgrid, ogrid, meshgrid

    Notes
    -----
    The output shape in the dense case is obtained by prepending the number
    of dimensions in front of the tuple of dimensions, i.e. if `dimensions`
    is a tuple ``(r0, ..., rN-1)`` of length ``N``, the output shape is
    ``(N, r0, ..., rN-1)``.

    The subarrays ``grid[k]`` contains the N-D array of indices along the
    ``k-th`` axis. Explicitly::

        grid[k, i0, i1, ..., iN-1] = ik

    Examples
    --------
    >>> import numpy as np
    >>> grid = np.indices((2, 3))
    >>> grid.shape
    (2, 2, 3)
    >>> grid[0]        # row indices
    array([[0, 0, 0],
           [1, 1, 1]])
    >>> grid[1]        # column indices
    array([[0, 1, 2],
           [0, 1, 2]])

    The indices can be used as an index into an array.

    >>> x = np.arange(20).reshape(5, 4)
    >>> row, col = np.indices((2, 3))
    >>> x[row, col]
    array([[0, 1, 2],
           [4, 5, 6]])

    Note that it would be more straightforward in the above example to
    extract the required elements directly with ``x[:2, :3]``.

    If sparse is set to true, the grid will be returned in a sparse
    representation.

    >>> i, j = np.indices((2, 3), sparse=True)
    >>> i.shape
    (2, 1)
    >>> j.shape
    (1, 3)
    >>> i        # row indices
    array([[0],
           [1]])
    >>> j        # column indices
    array([[0, 1, 2]])

    """
    dimensions = tuple(dimensions)
    N = len(dimensions)
    shape = (1,) * N
    if sparse:
        res = ()
    else:
        res = empty((N,) + dimensions, dtype=dtype)
    for i, dim in enumerate(dimensions):
        idx = arange(dim, dtype=dtype).reshape(
            shape[:i] + (dim,) + shape[i + 1:]
        )
        if sparse:
            res = res + (idx,)
        else:
            res[i] = idx
    return res


def indices(dimensions: Sequence[int], dtype: DTypeLike | None = None,
            sparse: Literal[False] = False) -> Array:
  ...


def indices(dimensions: Sequence[int], dtype: DTypeLike | None = None,
            *, sparse: Literal[True]) -> tuple[Array, ...]:
  ...


def indices(dimensions: Sequence[int], dtype: DTypeLike | None = None,
            sparse: bool = False) -> Array | tuple[Array, ...]:
  ...


def indices(dimensions: Sequence[int], dtype: DTypeLike | None = None,
            sparse: bool = False) -> Array | tuple[Array, ...]:
  """Generate arrays of grid indices.

  JAX implementation of :func:`numpy.indices`.

  Args:
    dimensions: the shape of the grid.
    dtype: the dtype of the indices (defaults to integer).
    sparse: if True, then return sparse indices. Default is False, which
      returns dense indices.

  Returns:
    An array of shape ``(len(dimensions), *dimensions)`` If ``sparse`` is False,
    or a sequence of arrays of the same length as ``dimensions`` if ``sparse`` is True.

  See also:
    - :func:`jax.numpy.meshgrid`: generate a grid from arbitrary input arrays.
    - :obj:`jax.numpy.mgrid`: generate dense indices using a slicing syntax.
    - :obj:`jax.numpy.ogrid`: generate sparse indices using a slicing syntax.

  Examples:
    >>> jnp.indices((2, 3))
    Array([[[0, 0, 0],
            [1, 1, 1]],
    <BLANKLINE>
           [[0, 1, 2],
            [0, 1, 2]]], dtype=int32)
    >>> jnp.indices((2, 3), sparse=True)
    (Array([[0],
           [1]], dtype=int32), Array([[0, 1, 2]], dtype=int32))
  """
  dtype = dtypes.check_and_canonicalize_user_dtype(
      int if dtype is None else dtype, "indices")
  dimensions = tuple(
      core.concrete_or_error(operator.index, d, "dimensions argument of jnp.indices")
      for d in dimensions)
  N = len(dimensions)
  output = []
  s = dimensions
  for i, dim in enumerate(dimensions):
    idx = lax.iota(dtype, dim)
    if sparse:
      s = (1,)*i + (dim,) + (1,)*(N - i - 1)
    output.append(lax.broadcast_in_dim(idx, s, (i,)))
  if sparse:
    return tuple(output)
  return stack(output, 0) if output else array([], dtype=dtype)

