
def _index_array(x, indexer: indexing.NDIndexer):
  if _is_trivial_indexer(indexer):
    return x
  # Try the three APIs in the following order: `lax.slice`,
  # `lax.dynamic_slice` and gather
  if maybe_slice := _maybe_convert_to_slice(indexer):
    x = lax_slicing.slice(x, *zip(*maybe_slice))
  # If everything in the indexer is a slice or ()-shaped, we can also
  # use `lax.dynamic_slice` with 1-sized slices for ()-shaped indices.
  # We need to squeeze out the 1-sized slices at the end.
  elif maybe_dynamic_slice := _maybe_convert_to_dynamic_slice(indexer):
    starts, sizes, squeeze_dims = maybe_dynamic_slice
    y = lax_slicing.dynamic_slice(x, starts, sizes)
    x = lax.squeeze(y, squeeze_dims)
  else:
    transpose_order = _maybe_transpose_before_gather(indexer)
    if transpose_order is not None:
      x, indexer = _perform_transpose_before_gather(x, indexer, transpose_order)
    arrays = _convert_to_gather_arrays(indexer)
    x = x[arrays]
  return x

