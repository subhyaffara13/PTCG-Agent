
def tile(A: ArrayLike, reps):
    if isinstance(reps, int):
        reps = (reps,)
    return torch.tile(A, reps)


def tile(g: jit_utils.GraphContext, self, dims):
    self_shape = g.op("Shape", self)
    self_rank = g.op("Size", self_shape)
    dims_rank = g.op("Size", dims)
    diff = g.op("Sub", self_rank, dims_rank)
    const_zero = g.op("Constant", value_t=torch.tensor([0]))

    # 1. If dims is shorter than self.shape pad dims with 1
    dims_shorter_than_self_shape = g.op("Greater", diff, const_zero)
    (
        if_op_greater,
        (if_context_greater, else_context_greater),
        _,
    ) = jit_utils.add_op_with_blocks(
        g, "If", dims_shorter_than_self_shape, n_blocks=2, outputs=1
    )
    const_one = if_context_greater.op("Constant", value_t=torch.LongTensor([1]))
    diff_1d_greater = if_context_greater.op("Reshape", diff, const_one)
    exapnd_ones_greater = if_context_greater.op("Expand", const_one, diff_1d_greater)
    dims_ = if_context_greater.op("Concat", exapnd_ones_greater, dims, axis_i=0)
    utils._add_output_to_block(if_context_greater.block, dims_)
    identity_dim = else_context_greater.op("Identity", dims)
    utils._add_output_to_block(else_context_greater.block, identity_dim)
    dims_final = if_op_greater.node().output()

    # 2. If dims is longer than self.shape pad self.shape with 1
    dims_longer_than_self_shape = g.op("Less", diff, const_zero)
    (
        if_op_less,
        (if_context_less, else_context_less),
        _,
    ) = jit_utils.add_op_with_blocks(
        g, "If", dims_longer_than_self_shape, n_blocks=2, outputs=1
    )
    const_one = if_context_less.op("Constant", value_t=torch.LongTensor([1]))
    diff_1d_less = if_context_less.op(
        "Reshape",
        if_context_less.op("Abs", diff),
        const_one,
    )
    exapnd_ones_less = if_context_less.op("Expand", const_one, diff_1d_less)
    self_final_shape = if_context_less.op(
        "Concat", exapnd_ones_less, self_shape, axis_i=0
    )
    self_ = if_context_less.op("Reshape", self, self_final_shape)
    utils._add_output_to_block(if_context_less.block, self_)
    identity_self = else_context_less.op("Identity", self)
    utils._add_output_to_block(else_context_less.block, identity_self)
    self_final = if_op_less.node().output()

    dims_final = g.op("Cast", dims_final, to_i=_C_onnx.TensorProtoDataType.INT64)
    return g.op("Tile", self_final, dims_final)


def tile(A, reps):
    """
    Construct an array by repeating A the number of times given by reps.

    If `reps` has length ``d``, the result will have dimension of
    ``max(d, A.ndim)``.

    If ``A.ndim < d``, `A` is promoted to be d-dimensional by prepending new
    axes. So a shape (3,) array is promoted to (1, 3) for 2-D replication,
    or shape (1, 1, 3) for 3-D replication. If this is not the desired
    behavior, promote `A` to d-dimensions manually before calling this
    function.

    If ``A.ndim > d``, `reps` is promoted to `A`.ndim by prepending 1's to it.
    Thus for an `A` of shape (2, 3, 4, 5), a `reps` of (2, 2) is treated as
    (1, 1, 2, 2).

    Note : Although tile may be used for broadcasting, it is strongly
    recommended to use numpy's broadcasting operations and functions.

    Parameters
    ----------
    A : array_like
        The input array.
    reps : array_like
        The number of repetitions of `A` along each axis.

    Returns
    -------
    c : ndarray
        The tiled output array.

    See Also
    --------
    repeat : Repeat elements of an array.
    broadcast_to : Broadcast an array to a new shape

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([0, 1, 2])
    >>> np.tile(a, 2)
    array([0, 1, 2, 0, 1, 2])
    >>> np.tile(a, (2, 2))
    array([[0, 1, 2, 0, 1, 2],
           [0, 1, 2, 0, 1, 2]])
    >>> np.tile(a, (2, 1, 2))
    array([[[0, 1, 2, 0, 1, 2]],
           [[0, 1, 2, 0, 1, 2]]])

    >>> b = np.array([[1, 2], [3, 4]])
    >>> np.tile(b, 2)
    array([[1, 2, 1, 2],
           [3, 4, 3, 4]])
    >>> np.tile(b, (2, 1))
    array([[1, 2],
           [3, 4],
           [1, 2],
           [3, 4]])

    >>> c = np.array([1,2,3,4])
    >>> np.tile(c,(4,1))
    array([[1, 2, 3, 4],
           [1, 2, 3, 4],
           [1, 2, 3, 4],
           [1, 2, 3, 4]])
    """
    try:
        tup = tuple(reps)
    except TypeError:
        tup = (reps,)
    d = len(tup)
    if all(x == 1 for x in tup) and isinstance(A, _nx.ndarray):
        # Fixes the problem that the function does not make a copy if A is a
        # numpy array and the repetitions are 1 in all dimensions
        return _nx.array(A, copy=True, subok=True, ndmin=d)
    else:
        # Note that no copy of zero-sized arrays is made. However since they
        # have no data there is no risk of an inadvertent overwrite.
        c = _nx.array(A, copy=None, subok=True, ndmin=d)
    if (d < c.ndim):
        tup = (1,) * (c.ndim - d) + tup
    shape_out = tuple(s * t for s, t in zip(c.shape, tup))
    n = c.size
    if n > 0:
        for dim_in, nrep in zip(c.shape, tup):
            if nrep != 1:
                c = c.reshape(-1, n).repeat(nrep, 0)
            n //= dim_in
    return c.reshape(shape_out)


def tile(operand: ArrayLike, reps: Sequence[int]) -> Array:
  """Tiles an array by repeating it along each dimension.

  Args:
    operand: an array to tile.
    reps: a sequence of integers representing the number of repeats for each
      dimension. Must have the same length as ``operand.ndim``.

  Returns:
    A tiled array with shape ``(operand.shape[0] * reps[0], ...,
    operand.shape[-1] * reps[-1])``.

  Examples:
    >>> x = jnp.array([[1, 2], [3, 4]])
    >>> lax.tile(x, (2, 3))
    Array([[1, 2, 1, 2, 1, 2],
           [3, 4, 3, 4, 3, 4],
           [1, 2, 1, 2, 1, 2],
           [3, 4, 3, 4, 3, 4]], dtype=int32)

    >>> y = jnp.array([1, 2, 3])
    >>> lax.tile(y, (2,))
    Array([1, 2, 3, 1, 2, 3], dtype=int32)

    >>> z = jnp.array([[1], [2]])
    >>> lax.tile(z, (1, 3))
    Array([[1, 1, 1],
           [2, 2, 2]], dtype=int32)
  """
  return tile_p.bind(operand, reps=tuple(reps))


def tile(A: ArrayLike, reps: DimSize | Sequence[DimSize]) -> Array:
  """Construct an array by repeating ``A`` along specified dimensions.

  JAX implementation of :func:`numpy.tile`.

  If ``A`` is an array of shape ``(d1, d2, ..., dn)`` and ``reps`` is a sequence of integers,
  the resulting array will have a shape of ``(reps[0] * d1, reps[1] * d2, ..., reps[n] * dn)``,
  with ``A`` tiled along each dimension.

  Args:
    A: input array to be repeated. Can be of any shape or dimension.
    reps: specifies the number of repetitions along each axis.

  Returns:
    a new array where the input array has been repeated according to ``reps``.

  See also:
    - :func:`jax.numpy.repeat`: Construct an array from repeated elements.
    - :func:`jax.numpy.broadcast_to`: Broadcast an array to a specified shape.

  Examples:
    >>> arr = jnp.array([1, 2])
    >>> jnp.tile(arr, 2)
    Array([1, 2, 1, 2], dtype=int32)
    >>> arr = jnp.array([[1, 2],
    ...                  [3, 4,]])
    >>> jnp.tile(arr, (2, 1))
    Array([[1, 2],
           [3, 4],
           [1, 2],
           [3, 4]], dtype=int32)
  """
  A = util.ensure_arraylike("tile", A)
  try:
    reps_tup = tuple(iter(reps))  # pyrefly: ignore[no-matching-overload]
  except TypeError:
    reps_tup: tuple[DimSize, ...] = (reps,)
  reps_tup = tuple(operator.index(rep) if core.is_constant_dim(rep) else rep
                   for rep in reps_tup)
  # lax.tile expects reps and A.shape to have the same rank.
  reps_tup = (1,) * (A.ndim - len(reps_tup)) + reps_tup
  if len(reps_tup) > np.ndim(A):
    A = lax.expand_dims(
        A, dimensions=tuple(range(len(reps_tup) - np.ndim(A))))
  return lax.tile(A, reps_tup)

