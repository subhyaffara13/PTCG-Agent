
def _addupdate_discharge(x, val, idx, tree):
  transforms = tree_util.tree_unflatten(tree, idx)
  if not transforms:
    return x + val
  if len(transforms) > 1:
    raise NotImplementedError("Only single indexer is supported.")
  indexer = transforms[0]

  if _is_trivial_indexer(indexer):
    return x + val

  # If everything in the indexer is a slice or ()-shaped, we can also
  # use `lax.dynamic_slice` with 1-sized slices for ()-shaped indices.
  # We need to squeeze out the 1-sized slices at the end.
  if maybe_slice := _maybe_convert_to_dynamic_slice(indexer):
    starts, sizes, squeeze_dims = maybe_slice
    x_old = lax_slicing.dynamic_slice(x, starts, sizes)
    val = lax.expand_dims(val, squeeze_dims)
    y = lax_slicing.dynamic_update_slice(x, x_old + val, starts)
    return y

  transpose_order = _maybe_transpose_before_gather(indexer)
  if transpose_order is not None:
    x, indexer = _perform_transpose_before_gather(x, indexer, transpose_order)
  arrays = _convert_to_gather_arrays(indexer)
  x = x.at[arrays].add(val)
  if transpose_order is not None:
    transpose_order_inversed = np.argsort(transpose_order)
    x = x.transpose(transpose_order_inversed)
  return x

