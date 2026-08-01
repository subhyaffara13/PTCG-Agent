
def transform_swap_array(x, transforms, val):
  if transforms is None:
    transforms = []

  # Will hold the value read from `x` before the swap, and will have the same
  # shape as `val`.
  new_val = x
  # List of intermediate results by transforming `x`.
  intermediates = [x]

  # Read phase (forward loop)
  for transform in transforms:
    match transform:
      case indexing.NDIndexer():
        indexer = transform
        if _is_trivial_indexer(indexer):
          intermediates.append(intermediates[-1])
          continue
        # If everything in the indexer is a slice or ()-shaped, we can also
        # use `lax.dynamic_slice` with 1-sized slices for ()-shaped indices.
        # We need to squeeze out the 1-sized slices at the end.
        if maybe_slice := _maybe_convert_to_dynamic_slice(indexer):
          starts, sizes, squeeze_dims = maybe_slice
          new_val = lax.squeeze(
              lax_slicing.dynamic_slice(new_val, starts, sizes), squeeze_dims
          )
        else:
          transpose_order = _maybe_transpose_before_gather(indexer)
          if transpose_order is not None:
            new_val, indexer = _perform_transpose_before_gather(
                new_val, indexer, transpose_order
            )
          arrays = _convert_to_gather_arrays(indexer)
          new_val = new_val[arrays]
          # Here, we don't need to transpose `new_val` back because it now holds
          # the result of the indexing, and is no longer the original array that
          # was indexed into.
        intermediates.append(new_val)
      case BitcastTransform():
        intermediates.append(bitcast(new_val, transform.dtype))
      case ReshapeTransform():
        intermediates.append(new_val.reshape(transform.shape))
      case _:
        raise NotImplementedError(f"Unsupported transform: {transform}")

  # Will hold the final state of the `x` after `val` has been written to the
  # transformed location, and will have the same shape as `x`.
  new_x = val

  # Write phase (reversed loop)
  for intermediate, transform in reversed(zip(intermediates[:-1], transforms)):
    if isinstance(transform, indexing.NDIndexer):
      indexer = transform
      if _is_trivial_indexer(indexer):
        continue
      if maybe_slice := _maybe_convert_to_dynamic_slice(indexer):
        starts, _, squeeze_dims = maybe_slice
        new_x = lax_slicing.dynamic_update_slice(
            intermediate, lax.expand_dims(new_x, squeeze_dims), starts
        )
      else:
        transpose_order = _maybe_transpose_before_gather(indexer)
        if transpose_order is not None:
          intermediate, indexer = _perform_transpose_before_gather(
              intermediate, indexer, transpose_order
          )
        arrays = _convert_to_gather_arrays(indexer)
        new_x = intermediate.at[arrays].set(new_x)
        if transpose_order is not None:
          transpose_order_inversed = np.argsort(transpose_order)
          new_x = new_x.transpose(transpose_order_inversed)
    else:
      raise NotImplementedError(f"Unsupported transform: {transform}")

  return new_val, new_x

