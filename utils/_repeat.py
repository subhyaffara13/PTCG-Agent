
def _repeat(self: Array, repeats: ArrayLike, axis: int | None = None, *,
            total_repeat_length: int | None = None,
            out_sharding: NamedSharding | PartitionSpec | None = None) -> Array:
  """Construct an array from repeated elements.

  Refer to :func:`jax.numpy.repeat` for the full documentation.
  """
  return lax_numpy.repeat(self, repeats=repeats, axis=axis,
                          total_repeat_length=total_repeat_length,
                          out_sharding=out_sharding)


def _repeat(repeats, arr, *, axis: int,
            total_repeat_length: int | None = None) -> Array:
  axis = core.concrete_or_error(operator.index, axis, "'axis' argument of jnp.repeat()")

  if core.is_symbolic_dim(repeats):
    if total_repeat_length is not None:
      raise ValueError("jnp.repeat with a non-constant `repeats` is supported only "
                       f"when `total_repeat_length` is None. ({repeats=} {total_repeat_length=})")

  # If total_repeat_length is not given, use a default.
  if total_repeat_length is None:
    repeats = core.concrete_or_error(None, repeats,
      "When jit-compiling jnp.repeat, the total number of repeats must be static. "
      "To fix this, either specify a static value for `repeats`, or pass a static "
      "value to `total_repeat_length`.")

    # Fast path for when repeats is a scalar.
    if np.ndim(repeats) == 0 and np.ndim(arr) != 0:
      input_shape = arr.shape
      axis = _canonicalize_axis(axis, len(input_shape))
      aux_axis = axis + 1
      aux_shape: list[DimSize] = list(input_shape)
      aux_shape.insert(aux_axis, operator.index(repeats) if core.is_constant_dim(repeats) else repeats)
      arr = lax.broadcast_in_dim(
        arr, aux_shape, [i for i in range(len(aux_shape)) if i != aux_axis])
      result_shape: list[DimSize] = list(input_shape)
      result_shape[axis] *= repeats
      return arr.reshape(result_shape)

    repeats = np.ravel(repeats)
    if arr.ndim != 0:
      repeats = np.broadcast_to(repeats, [arr.shape[axis]])
    total_repeat_length = int(np.sum(repeats))
  else:
    repeats = ravel(repeats)
    if arr.ndim != 0:
      repeats = broadcast_to(repeats, [arr.shape[axis]])

  # Special case when a is a scalar.
  if arr.ndim == 0:
    if np.shape(repeats) == (1,):
      return array_creation.full([total_repeat_length], arr)
    else:
      raise ValueError('`repeat` with a scalar parameter `a` is only '
      'implemented for scalar values of the parameter `repeats`.')

  # Special case if total_repeat_length is zero.
  if total_repeat_length == 0:
    result_shape = list(arr.shape)
    result_shape[axis] = 0
    return reshape(array([], dtype=arr.dtype), result_shape)

  # If repeats is on a zero sized axis, then return the array.
  if arr.shape[axis] == 0:
    return arr

  # This implementation of repeat avoid having to instantiate a large.
  # intermediate tensor.

  # Modify repeats from e.g. [1,2,0,5] -> [0,1,2,0] for exclusive repeat.
  exclusive_repeats = roll(repeats, shift=1).at[0].set(0)
  # Cumsum to get indices of new number in repeated tensor, e.g. [0, 1, 3, 3]
  scatter_indices = reductions.cumsum(exclusive_repeats)
  # Scatter these onto a zero buffer, e.g. [1,1,0,2,0,0,0,0]
  block_split_indicators = array_creation.zeros([total_repeat_length], dtype='int32')
  block_split_indicators = block_split_indicators.at[scatter_indices].add(1)
  # Cumsum again to get scatter indices for repeat, e.g. [0,1,1,3,3,3,3,3]
  gather_indices = reductions.cumsum(block_split_indicators) - 1
  return indexing.take(arr, gather_indices, axis=axis)

