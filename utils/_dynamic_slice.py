
def _dynamic_slice(arr: Array, indexer: _DynamicSliceIndexer) -> Array:
  """Equivalent of arr[idx] implemented in terms of static :func:`lax.dynamic_slice`.

  This supports only INTEGER, ELLIPSIS, NONE, SLICE, and scalar ARRAY indices,
  and will raise a TypeError if other indices are present.
  """
  if indexer.trivial_slicing:
    result = arr
  else:
    result = slicing.dynamic_slice(
      arr,
      start_indices=indexer.start_indices,
      slice_sizes=indexer.slice_sizes,
      allow_negative_indices=indexer.normalize_indices)
  if indexer.rev_axes:
    result = lax.rev(result, indexer.rev_axes)
  if indexer.squeeze_axes:
    result = lax.squeeze(result, indexer.squeeze_axes)
  if indexer.newaxis_dims:
    result = lax.expand_dims(result, indexer.newaxis_dims)
  return result


def _dynamic_slice(
    start_idx, block_shape: tuple[int, ...], value, is_squeeze,
):
  start_idx = tuple(jnp.asarray(s, dtype=jnp.int32) for s in start_idx)
  output = slicing.dynamic_slice(value, start_idx, slice_sizes=block_shape)
  squeeze_dims = tuple(np.arange(len(is_squeeze))[np.array(is_squeeze,
                                                           dtype=np.bool_)])
  return lax.squeeze(output, squeeze_dims)

