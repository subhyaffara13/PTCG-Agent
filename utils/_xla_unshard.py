
def _xla_unshard(ctx: mlir.LoweringRuleContext, mesh, manual_axes, spec,
                 aval_in, aval_out, x):
  if prod([size for n, size in mesh.shape.items() if n in manual_axes]) == 1:
    return x
  ns = _make_scoped_manual_sharding(ctx, mesh, spec)
  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):
    ns = sharding_impls.physical_sharding(aval_out, ns)
    aval_out = core.physical_aval(aval_out)
  unspecified = (set(range(aval_in.ndim))
                 if len(manual_axes) < len(mesh.axis_names) else set())
  if dtypes.issubdtype(aval_in.dtype, dtypes.extended):
    aval_in = core.physical_aval(aval_in)
  manual_proto = pxla.manual_proto(
      aval_in, manual_axes | set(mesh.manual_axes), mesh)
  sx = mlir.wrap_with_sharding_op(ctx, x, aval_in, manual_proto,
                                  unspecified_dims=unspecified)
  shard_proto = ns._to_xla_hlo_sharding(aval_out.ndim).to_proto()
  return mlir.wrap_with_shard_to_full_op(ctx, sx, aval_out, shard_proto,
                                         unspecified)

