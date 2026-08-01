
def _barrier_wait_lowering(
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
  barrier.wait(orders_tensor_core=orders_tensor_core)
  return ()

