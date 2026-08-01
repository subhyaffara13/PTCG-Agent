
def _to_physical_op_sharding(
    ctx: ModuleContext,
    aval: core.AbstractValue, sharding: JSharding | None,
) -> xc.OpSharding | SdyArray | None:
  if sharding is None:
    return None
  if all_unconstrained(sharding, aval):
    return None
  assert isinstance(sharding, JSharding)
  if isinstance(aval, AbstractRef):
    return _to_physical_op_sharding(ctx, aval.inner_aval, sharding)
  assert isinstance(aval, core.ShapedArray)
  if dtypes.issubdtype(aval.dtype, dtypes.extended):
    sharding = sharding_impls.physical_sharding(aval, sharding)
    aval = core.physical_aval(aval)
  axis_ctx = ctx.axis_context
  if (isinstance(axis_ctx, sharding_impls.SPMDAxisContext) and
      axis_ctx.manual_axes):
    sharding = add_manual_axes(axis_ctx, sharding, aval.ndim)
  if config.use_shardy_partitioner.value:
    return sharding._to_sdy_sharding(aval.ndim)
  return sharding._to_xla_hlo_sharding(aval.ndim).to_proto()

