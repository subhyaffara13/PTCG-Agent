
def _core_map_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    jaxpr,
    mesh,
    **_,
):
  if not isinstance(mesh, gpu_core.WarpMesh):
    raise NotImplementedError(f"Unsupported mesh: {mesh}")
  # A core_map over a WarpMesh represents a fork/join over individual
  # warps in a warpgroup.
  if (ctx.module_ctx.warp_axis_name or
      ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp):
    raise LoweringError(
        "Cannot nest core_maps. Already under core_map with warp_axis_name "
        f"{ctx.module_ctx.warp_axis_name}.")
  module_ctx = dataclasses.replace(
      ctx.module_ctx,
      warp_axis_name=mesh.axis_name,
      primitive_semantics=gpu_core.PrimitiveSemantics.Warp,
  )
  for aval_in in ctx.avals_in:
    if isinstance(aval_in, jax_core.ShapedArray) and aval_in.shape:
      raise LoweringError(
        "Can only close over scalars and Refs when using core_map with "
        f"WarpMesh. Found array of shape {aval_in}."
      )
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    # We allow the warps to schedule async copies without synchronizing with
    # other warps, so we need to add a barrier here to make sure all reads and
    # writes have completed.
    if ctx.module_ctx.auto_barriers:
      mgpu.warpgroup_barrier()
    _ = lower_jaxpr_to_mosaic_gpu(
        module_ctx,
        ctx.launch_ctx,
        jaxpr,
        args=(),
        consts=args,
    )
    if ctx.module_ctx.auto_barriers:
      # We need to ensure that any effects produced by one warp
      # (e.g. async copies) are observable by all other warps.
      mgpu.warpgroup_barrier()
  else:
    warp_map_op = mgpu.dialect.WarpMapOp(operands=[])
    with ir.InsertionPoint(warp_map_op.body):
      _ = lower_jaxpr_to_mosaic_gpu(
          module_ctx,
          ctx.launch_ctx,
          jaxpr,
          args=(),
          consts=args,
      )
    _isolate_from_above(warp_map_op)
  return []

