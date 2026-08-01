
def _static_slice(arr: Array, indexer: _StaticSliceIndexer) -> Array:
  """Equivalent of arr[idx] implemented in terms of static :func:`lax.slice` operations.

  This supports only INTEGER, ELLIPSIS, NONE, and SLICE indices, and will raise a
  TypeError if other indices are present.
  """
  if indexer.is_trivial_slice(arr.shape):
    result = arr
  else:
    result = slicing.slice(arr, indexer.start_indices,
                            indexer.limit_indices, indexer.strides)
  if indexer.rev_axes:
    result = lax.rev(result, indexer.rev_axes)
  if indexer.squeeze_axes:
    result = lax.squeeze(result, indexer.squeeze_axes)
  if indexer.newaxis_dims:
    result = lax.expand_dims(result, indexer.newaxis_dims)
  return result

