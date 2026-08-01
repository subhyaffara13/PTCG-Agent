
def _scatter_abstract_eval(*flat_args, tree, add):
  ref, transforms, indices, x, mask = jax.tree.unflatten(tree, flat_args)
  if transforms:
    ref = state_types.TransformedRef(ref, transforms)
  if ref.dtype not in (jnp.int32, jnp.float32):
    raise TypeError(f"ref.dtype={ref.dtype} must be int32 or float32")
  expected_shape = _indexed_shape(ref, indices)
  if x.shape != expected_shape:
    raise ValueError(
        f"{x.shape=} does not match expected shape {expected_shape}"
    )
  if x.dtype != ref.dtype:
    raise TypeError(f"val.dtype={x.dtype} != ref.dtype={ref.dtype}")
  if mask is not None and mask.shape != expected_shape:
    raise ValueError(
        f"{mask.shape=} does not match expected shape {expected_shape}"
    )
  effects: set[jax_core.Effect] = {state_types.WriteEffect(0)}
  if add:
    effects.add(state_types.ReadEffect(0))
  return (), effects

