
def _load_abstract_eval(*avals_flat, args_tree, **_):
  ref_aval, transforms, mask_aval, _ = args_tree.unflatten(avals_flat)
  assert transforms is not None
  transformed_ref = pallas_core.TransformedRef(ref_aval, transforms)
  if mask_aval is not None:
    try:
      # pyrefly: ignore[no-matching-overload]
      jnp.broadcast_shapes(transformed_ref.shape, mask_aval.shape)
    except ValueError:
      raise ValueError(
          f"Cannot broadcast mask shape {mask_aval.shape} to load shape"
          f" {transformed_ref.shape}"
      )
  return (
      jax_core.ShapedArray(transformed_ref.shape, transformed_ref.dtype),
      {state.ReadEffect(0)},
  )


def _load_abstract_eval(ref, *args, has_mask, tree):
  flat_transforms = args[:-1] if has_mask else args
  tref = state_types.TransformedRef(
      ref, jax.tree.unflatten(tree, flat_transforms))
  if has_mask:
    mask = args[-1]
    if mask.dtype != jnp.bool:
      raise TypeError(f"Mask must be a boolean array, got {mask.dtype}")
    if mask.shape != tref.shape:
      raise ValueError(f"Mask must have shape {tref.shape}, got {mask.shape}")
  return (
      jax_core.ShapedArray(tref.shape, ref.dtype), {state_types.ReadEffect(0)})


def _load_abstract_eval(src, *avals_flat, tree, optimized):
  del optimized  # Unused.
  transforms = list(tree.unflatten(avals_flat))
  if not transforms or not isinstance(transforms[-1], indexing.NDIndexer):
    tref_aval = state.transform_type(transforms, src)
    assert isinstance(tref_aval, state_types.AbstractRef)
    transforms.append(indexing.NDIndexer.make_trivial_indexer(tref_aval.shape))
  out_ty = state.transform_type(transforms, src)
  assert isinstance(out_ty, state_types.AbstractRef)
  return out_ty.inner_aval, {state.ReadEffect(0)}

