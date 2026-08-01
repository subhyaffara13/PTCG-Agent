
def _semaphore_signal_multicast_lowering(
    ctx: lowering.LoweringRuleContext, *args, args_tree, collective_axes
):
  sem, transforms, value = tree_util.tree_unflatten(args_tree, args)
  sem_aval, transform_avals, _ = tree_util.tree_unflatten(args_tree, ctx.avals_in)
  assert isinstance(sem_aval, state_types.AbstractRef)
  sem, _, sem_transforms = lowering._handle_transforms(ctx, sem_aval, sem,
                                                       transform_avals,
                                                       transforms)
  if sem_transforms:
    raise NotImplementedError(
        f"Unhandled transforms for semaphore_signal_multicast: {sem_transforms}"
    )
  if not isinstance(collective_axes, (tuple, list)):
    collective_axes = (collective_axes,)
  if (mesh_info := ctx.module_ctx.mesh_info) is None:
    raise ValueError("collective_axes requires a mesh context")
  if set(collective_axes) != set(mesh_info.axis_names):
    raise ValueError(
        f"collective_axes {collective_axes} must equal entire mesh axes {mesh_info.axis_names}"
    )
  i32 = ir.IntegerType.get_signless(32)
  val = lowering._ir_constant(value, i32)
  multi_ref = ctx.launch_ctx.to_remote_multicast(sem).ref
  with lowering._wrap_in_custom_primitive_if_wg(ctx, [multi_ref, val]) as [multi_ref, val]:
    if ctx.module_ctx.auto_barriers:
      if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
        mgpu_utils.warp_barrier()
      else:
        mgpu_utils.warpgroup_barrier()

    assert ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane
    predicate = ctx.module_ctx.single_lane_predicate

    mgpu_utils.SemaphoreRef.signal_multimem(
        mgpu_utils.memref_ptr(multi_ref), val, predicate=predicate
    )
  return ()

