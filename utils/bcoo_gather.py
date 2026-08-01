
def bcoo_gather(operand: BCOO, start_indices: Array,
                dimension_numbers: GatherDimensionNumbers,
                slice_sizes: Shape, *,
                unique_indices: bool = False,
                indices_are_sorted: bool = False,
                mode: str | GatherScatterMode | None = None,
                fill_value = None) -> BCOO:
  """BCOO version of lax.gather."""
  _validate_bcoo(operand.data, operand.indices, operand.shape)

  # TODO(jakevdp) make use of unique_indices and indices_are_sorted?
  if mode is None:
    mode = GatherScatterMode.PROMISE_IN_BOUNDS
  parsed_mode = GatherScatterMode.from_any(mode)
  if parsed_mode != GatherScatterMode.PROMISE_IN_BOUNDS:
    raise NotImplementedError(f"bcoo_gather: {mode=} not yet supported.")

  kwds = dict(dimension_numbers=dimension_numbers, slice_sizes=slice_sizes,
              unique_indices=unique_indices, indices_are_sorted=indices_are_sorted,
              mode=mode, fill_value=fill_value)

  # Abstract eval lax.gather to validate arguments & determine output shape.
  static_argnames = ("dimension_numbers", "slice_sizes", "unique_indices",
          "indices_are_sorted", "mode", "fill_value",)
  out_aval = jax.jit(lax.gather, static_argnames=static_argnames).eval_shape(
          jax.ShapeDtypeStruct(operand.shape, operand.dtype),
          jax.ShapeDtypeStruct(start_indices.shape, start_indices.dtype),
          **kwds)

  offset_dims = dimension_numbers.offset_dims
  collapsed_slice_dims = dimension_numbers.collapsed_slice_dims
  start_index_map = dimension_numbers.start_index_map

  # Expand start_indices & slice_sizes to full rank & use bcoo_dynamic_slice
  full_start_indices: list[ArrayLike] = [_const(start_indices, 0)] * operand.ndim
  in_axes: list[int | None] = [None for i in range(operand.ndim)]
  full_slice_sizes = list(operand.shape)
  for i, j in enumerate(start_index_map):
    full_start_indices[j] = start_indices[..., i].ravel()
    full_slice_sizes[j] = slice_sizes[j]
    in_axes[j] = 0
  def slice_func(indices):
    slc = bcoo_dynamic_slice(operand, indices, slice_sizes=full_slice_sizes)
    return bcoo_squeeze(slc, dimensions=collapsed_slice_dims)
  result = vmap(slice_func, in_axes=(in_axes,))(full_start_indices)
  result = bcoo_reshape(result,
    new_sizes=(*start_indices.shape[:-1], *result.shape[1:]),
    dimensions=tuple(range(result.ndim)))

  # Use offset_dims to permute result dimensions
  if result.shape:
    batch_dims = tuple(dim for dim in range(len(out_aval.shape))
                      if dim not in offset_dims)
    permutation = np.zeros(result.ndim, dtype=int)
    permutation[np.array(batch_dims + offset_dims)] = np.arange(result.ndim)
    if set(permutation[:len(batch_dims)]) != set(range(len(batch_dims))):
      # TODO: jakevdp more granular approach here. Can we do this in a
      # way that preserves the original batch dimensions?
      result = bcoo_update_layout(result, n_batch=0)
    result = bcoo_transpose(result, permutation=tuple(permutation))

  return result.reshape(out_aval.shape).astype(out_aval.dtype)

