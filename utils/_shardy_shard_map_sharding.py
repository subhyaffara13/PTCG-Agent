
def _shardy_shard_map_sharding(
    ctx: mlir.LoweringRuleContext, mesh, manual_axes, spec, aval_in
) -> sharding_impls.SdyArray:
  ns = _make_scoped_manual_sharding(ctx, mesh, spec)
  if dtypes.issubdtype(aval_in.dtype, dtypes.extended):
    ns = sharding_impls.physical_sharding(aval_in, ns)
    aval_in = core.physical_aval(aval_in)
  if len(manual_axes) < len(mesh.axis_names):
    # In partial manual case, mark all dims as open.
    return ns._to_sdy_sharding(aval_in.ndim, modify_wrt_axis_types=True)
  else:
    return ns._to_sdy_sharding(aval_in.ndim)

