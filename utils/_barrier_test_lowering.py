
def _barrier_test_lowering(
    ctx: lowering.LoweringRuleContext,
    barrier,
    *flat_transforms,
    transforms_treedef,
):
  barrier_aval = ctx.avals_in[0]
  assert isinstance(barrier_aval, state_types.AbstractRef)
  transforms = transforms_treedef.unflatten(flat_transforms)
  orders_tensor_core = getattr(
      barrier_aval.inner_aval.dtype, "orders_tensor_core", False  # pyrefly: ignore[missing-attribute]
  )
  base_index = _get_barrier_base_index(barrier_aval, transforms)
  if base_index is not None:
    barrier = barrier[base_index]
  # Ensure that all threads in the warp have converged and will not read
  # different values from the barrier.
  mgpu.utils.warp_barrier()
  wait_complete = barrier.test(orders_tensor_core=orders_tensor_core)
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
    return wait_complete
  return mgpu.FragmentedArray.splat(wait_complete, shape=(), is_signed=False)

