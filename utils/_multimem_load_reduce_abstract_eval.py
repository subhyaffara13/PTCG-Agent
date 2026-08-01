
def _multimem_load_reduce_abstract_eval(ref, *avals_flat, tree, collective_axes, reduction_op):
  del collective_axes, reduction_op
  _check_ref(ref, "ref", gpu_core.GMEM)
  out_ref = ref
  if tree is not None:
    transforms = jax.tree.unflatten(tree, avals_flat)
    out_ref = state.transform_type(transforms, ref)
  assert isinstance(out_ref, state_types.AbstractRef)
  return out_ref.inner_aval, {pallas_core.comms_effect}

