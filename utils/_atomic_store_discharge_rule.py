
def _atomic_store_discharge_rule(
    in_avals, out_avals, *args_flat, args_tree, atomic_type: AtomicOpType
):
  del out_avals
  ref, transforms, val, mask = args_tree.unflatten(args_flat)
  *prev_transforms, idx = transforms
  ref = discharge.transform_array(ref, prev_transforms)

  if mask is not None:
    raise NotImplementedError

  if atomic_type == AtomicOpType.ADD:
    monoid = lambda x, y: x + y
  elif atomic_type == AtomicOpType.MAX:
    monoid = jnp.maximum
  elif atomic_type == AtomicOpType.MIN:
    monoid = jnp.minimum
  else:
    raise NotImplementedError(atomic_type)

  if all(
      (isinstance(s, indexing.Slice) or not s.shape) for s in idx.indices
  ):
    indices = idx.indices
    scalar_dims = [
        not isinstance(s, indexing.Slice) and not s.shape for s in indices
    ]
    slice_starts = [
        s.start if isinstance(s, indexing.Slice) else s for s in indices
    ]
    slice_sizes = tuple(
        s.size if isinstance(s, indexing.Slice) else 1 for s in indices
    )
    out_ones = lax.dynamic_slice(ref, slice_starts, slice_sizes=slice_sizes)
    val_indexer = tuple(
        None if scalar else slice(None) for scalar in scalar_dims
    )
    val = val[val_indexer]
    val = monoid(val, out_ones)
    x_new = lax.dynamic_update_slice(ref, val, start_indices=slice_starts)
  elif all(not isinstance(s, indexing.Slice) for s in idx.indices):
    out = ref[idx.indices]
    x_new = ref.at[idx.indices].set(monoid(out, val))
  else:
    raise NotImplementedError
  return (x_new,) + (None,) * (len(in_avals) - 1), ()

