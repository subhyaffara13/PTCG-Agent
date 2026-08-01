
def _take(self: Array, indices: ArrayLike, axis: int | None = None, out: None = None,
          mode: str | None = None, unique_indices: bool = False, indices_are_sorted: bool = False,
          fill_value: StaticScalar | None = None) -> Array:
  """Take elements from an array.

  Refer to :func:`jax.numpy.take` for full documentation.
  """
  return indexing.take(self, indices, axis=axis, out=out, mode=mode, unique_indices=unique_indices,
                       indices_are_sorted=indices_are_sorted, fill_value=fill_value)


def _take(a, indices, axis: int | None = None, out=None, mode=None,
          unique_indices=False, indices_are_sorted=False, fill_value=None):
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.take is not supported.")
  a, indices = util.ensure_arraylike("take", a, indices)

  if axis is None:
    a = a.ravel()
    axis_idx = 0
  else:
    axis_idx = canonicalize_axis(axis, np.ndim(a))

  if mode is None or mode == "fill":
    gather_mode = slicing.GatherScatterMode.FILL_OR_DROP
    # lax.gather() does not support negative indices, so we wrap them here
    indices = util._where(indices < 0, indices + a.shape[axis_idx], indices)
  elif mode == "raise":
    # TODO(phawkins): we have no way to report out of bounds errors yet.
    raise NotImplementedError("The 'raise' mode to jnp.take is not supported.")
  elif mode == "wrap":
    indices = ufuncs.mod(indices, lax._const(indices, a.shape[axis_idx]))
    gather_mode = slicing.GatherScatterMode.PROMISE_IN_BOUNDS
  elif mode == "clip":
    gather_mode = slicing.GatherScatterMode.CLIP
  else:
    raise ValueError(f"Invalid mode '{mode}' for np.take")

  index_dims = len(np.shape(indices))
  slice_sizes = list(np.shape(a))
  if slice_sizes[axis_idx] == 0:
    if indices.size != 0:
      raise IndexError("Cannot do a non-empty jnp.take() from an empty axis.")
    return a

  if indices.size == 0:
    out_shape = (slice_sizes[:axis_idx] + list(indices.shape) +
                 slice_sizes[axis_idx + 1:])
    return lax.full_like(a, 0, shape=out_shape)

  slice_sizes[axis_idx] = 1
  dnums = slicing.GatherDimensionNumbers(
    offset_dims=tuple(
      list(range(axis_idx)) +
      list(range(axis_idx + index_dims, len(a.shape) + index_dims - 1))),
    collapsed_slice_dims=(axis_idx,),
    start_index_map=(axis_idx,))
  return slicing.gather(a, indices[..., None], dimension_numbers=dnums,
                        slice_sizes=tuple(slice_sizes),
                        mode=gather_mode, unique_indices=unique_indices,
                        indices_are_sorted=indices_are_sorted, fill_value=fill_value)

