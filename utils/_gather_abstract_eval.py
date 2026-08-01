
def _gather_abstract_eval(*flat_args, tree):
  ref, transforms, indices, mask = tree.unflatten(flat_args)
  if transforms:
    ref = state_types.TransformedRef(ref, transforms)
  if ref.dtype not in (jnp.int32, jnp.float32):
    raise TypeError(f"ref.dtype={ref.dtype} must be int32 or float32")
  out_aval = jax_core.ShapedArray(_indexed_shape(ref, indices), ref.dtype)
  sc_lowering._check_aval_is_supported("Gather", out_aval)
  if mask is not None and mask.shape != out_aval.shape:
    raise ValueError(
        f"{mask.shape=} does not match the expected shape {out_aval.shape}"
    )
  return out_aval, {state_types.ReadEffect(0)}

