
def _swap_discharge_rule(in_avals, out_avals, *args_flat, args_tree, **_):
  del out_avals  # Unused.
  ref, transforms, val, mask = args_tree.unflatten(args_flat)
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
    scalar_dims = [
        i
        for i, s in enumerate(indices)
        if not isinstance(s, Slice) and not s.shape  # pyrefly: ignore[missing-attribute]
    ]
    slice_starts = [s.start if isinstance(s, Slice) else s for s in indices]
    slice_sizes = tuple(s.size if isinstance(s, Slice) else 1 for s in indices)
    # Fixes an inconsistency with lax.dynamic_update_slice where if the slice
    # goes out of bounds, it will instead move the start_index backwards so the
    # slice will fit in memory.
    ref = _pad_values_to_avoid_dynamic_slice_oob_shift(ref, slice_sizes)
    out = lax.dynamic_slice(ref, slice_starts, slice_sizes=slice_sizes)
    out = jnp.squeeze(out, scalar_dims)
    if mask is not None:
      out_ = out
      out = jnp.where(mask, out, val)
      val = jnp.where(mask, val, out_)
    val = jnp.expand_dims(val, scalar_dims)
    x_new = lax.dynamic_update_slice(ref, val, start_indices=slice_starts)
    x_new = _unpad_values_to_avoid_dynamic_slice_oob_shift(x_new, slice_sizes)
  elif all(not isinstance(s, Slice) for s in idx.indices):
    out = ref[idx.indices]
    if mask is not None:
      out_ = out
      out = jnp.where(mask, out, val)
      val = jnp.where(mask, val, out_)
    x_new = ref.at[idx.indices].set(val)
  else:
    raise NotImplementedError
  return (x_new,) + (None,) * (len(in_avals) - 1), out


def _swap_discharge_rule(
    in_avals: Sequence[core.AbstractValue],
    out_avals: Sequence[core.AbstractValue], x, val, *idx,
    tree):
  del in_avals, out_avals
  z, x_new = _swap_discharge(x, val, idx, tree)
  return (x_new, None) + (None,) * len(idx), z

