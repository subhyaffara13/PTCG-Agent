
def _gather(arr, dynamic_idx, *, treedef, indices_are_sorted,
            unique_indices, mode, fill_value, normalize_indices):
  parsed_idx = tree_unflatten(treedef, dynamic_idx)
  indexer = parsed_idx.to_gather(core.typeof(arr).sharding,
                                 normalize_indices=normalize_indices)
  jnp_error._check_precondition_oob_gather(arr.shape, indexer.gather_indices)
  y = arr

  if fill_value is not None:
    core.concrete_or_error(None, fill_value,
                           "fill_value argument to indexed get()")
    if np.ndim(fill_value) != 0:
      raise ValueError("fill_value argument to indexed get() must be a scalar")
    if isinstance(fill_value, np.ndarray):
      fill_value = fill_value.item()

  if indexer.scalar_bool_dims:
    y = lax.expand_dims(y, indexer.scalar_bool_dims)

  # Avoid calling gather if the slice shape is empty, both as a fast path and to
  # handle cases like zeros(0)[array([], int32)].
  if core.is_empty_shape(indexer.slice_shape):
    return lax.full_like(y, 0, shape=indexer.slice_shape,
                         sharding=indexer.slice_sharding)

  # We avoid generating a gather when indexer.gather_indices.size is empty.
  if not core.is_empty_shape(indexer.gather_indices.shape):
    y = slicing.gather(
        y, indexer.gather_indices, indexer.dnums, indexer.gather_slice_shape,
        unique_indices=unique_indices or indexer.unique_indices,
        indices_are_sorted=indices_are_sorted or indexer.indices_are_sorted,
        mode=mode, fill_value=fill_value)

  # Reverses axes with negative strides.
  if indexer.reversed_y_dims:
    y = lax.rev(y, indexer.reversed_y_dims)
  # This adds np.newaxis/None dimensions.
  return lax.expand_dims(y, indexer.newaxis_dims)

