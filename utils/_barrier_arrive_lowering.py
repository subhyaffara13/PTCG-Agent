
def _barrier_arrive_lowering(
    ctx: lowering.LoweringRuleContext,
    barrier,
    *flat_transforms,
    transforms_treedef,
):
  transforms = transforms_treedef.unflatten(flat_transforms)
  barrier_aval = ctx.avals_in[0]
  assert isinstance(barrier_aval, state_types.AbstractRef)
  base_index = _get_barrier_base_index(barrier_aval, transforms)
  if base_index is not None:
    barrier = barrier[base_index]
  sem_dtype = barrier_aval.inner_aval.dtype  # pyrefly: ignore[missing-attribute]
  orders_tensor_core = getattr(sem_dtype, "orders_tensor_core", False)

  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    scope = mgpu_utils.ThreadSubset.WARP
  else:
    scope = mgpu_utils.ThreadSubset.WARPGROUP

  if isinstance(barrier, mgpu.CollectiveBarrierRef):
    if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
      raise NotImplementedError(
          "Arriving on a collective barrier is not supported in a warp context"
      )
    barrier.arrive(orders_tensor_core)
  elif ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
    barrier.arrive(orders_tensor_core)
  else:
    if scope == mgpu_utils.ThreadSubset.WARP and not orders_tensor_core:
      arrival_count = 4
    else:
      arrival_count = 1

    pred = ctx.module_ctx.single_lane_predicate if orders_tensor_core else None
    barrier.arrive(
        arrival_count=arrival_count,
        orders_tensor_core=orders_tensor_core,
        predicate=pred,
        scope=scope,
    )
  return ()

