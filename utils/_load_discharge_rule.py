
def _load_discharge_rule(in_avals, out_avals, *args_flat, args_tree, **_):
  del out_avals  # Unused.
  ref, transforms, mask, other = args_tree.unflatten(args_flat)
  transforms = list(transforms)
  if not transforms or not isinstance(transforms[-1], indexing.NDIndexer):
    ref_aval = state.transform_type(transforms, in_avals[0])
    assert isinstance(ref_aval, state.AbstractRef)
    transforms.append(indexing.NDIndexer.make_trivial_indexer(ref_aval.shape))
  *prev_transforms, idx = transforms
  assert isinstance(idx, NDIndexer)
  ref = state_discharge.transform_array(ref, prev_transforms)
  if all((isinstance(s, Slice) or not s.shape) for s in idx.indices):  # pyrefly: ignore[missing-attribute]
    # TODO(ayx): support strided load/store in interpret mode.
    for s in idx.indices:
      if isinstance(s, Slice) and s.stride > 1:
        raise NotImplementedError("Unimplemented stride support.")
    indices = idx.indices
    scalar_dims = [not isinstance(s, Slice) and not s.shape for s in indices]  # pyrefly: ignore[missing-attribute]
    slice_starts = [s.start if isinstance(s, Slice) else s for s in indices]
    slice_sizes = tuple(s.size if isinstance(s, Slice) else 1 for s in indices)
    # fixes an inconsistency with lax.dynamic_slice where if the slice goes out
    # of bounds, it will instead move the start_index backwards so the slice
    # will fit in memory.
    ref = _pad_values_to_avoid_dynamic_slice_oob_shift(ref, slice_sizes)
    idx_dtype = dtypes.default_int_dtype()
    out_ones = lax.dynamic_slice(
        ref,
        [jnp.astype(s, idx_dtype) for s in slice_starts],
        slice_sizes=slice_sizes,
    )
    out_indexer = tuple(0 if scalar else slice(None) for scalar in scalar_dims)
    out = out_ones[out_indexer]
  elif all(not isinstance(s, Slice) for s in idx.indices):
    out = ref[idx.indices]
  else:
    raise NotImplementedError
  if mask is not None and other is not None:
    out = jnp.where(mask, out, other)
  return (None,) * len(in_avals), out

