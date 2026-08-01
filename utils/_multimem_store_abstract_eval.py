
def _multimem_store_abstract_eval(source, ref, *transforms_leaves, transforms_tree, **_):
  _check_ref(ref, "ref", gpu_core.GMEM)
  shape, dtype = ref.shape, ref.dtype
  if transforms_tree is not None:
    transforms = jax.tree.unflatten(transforms_tree, transforms_leaves)
    ty = state.transform_type(transforms, ref)
    assert isinstance(ty, state.AbstractRef)
    shape = ty.shape
    dtype = ty.dtype
  if source.dtype != dtype:
    raise ValueError(f"Value dtype {source.dtype} does not match ref dtype {dtype}")
  if source.shape != shape:
    raise ValueError(f"Value shape {source.shape} does not match ref shape {shape}")
  return [], {pallas_core.comms_effect, state.WriteEffect(1)}

