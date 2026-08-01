
def _xla_shard(ctx: mlir.LoweringRuleContext, mesh, manual_axes, spec,
               aval_in, aval_out, x):
  if prod([size for n, size in mesh.shape.items() if n in manual_axes]) == 1:
    return x
  ns = _make_scoped_manual_sharding(ctx, mesh, spec)
  if dtypes.issubdtype(aval_in.dtype, dtypes.extended):
    ns = sharding_impls.physical_sharding(aval_in, ns)
    aval_in = core.physical_aval(aval_in)
  shard_proto = ns._to_xla_hlo_sharding(aval_in.ndim).to_proto()
  unspecified = (set(range(aval_in.ndim))
                 if len(manual_axes) < len(mesh.axis_names) else set())
  sx = mlir.wrap_with_sharding_op(ctx, x, aval_in, shard_proto,
                                  unspecified_dims=unspecified)
  manual_proto = pxla.manual_proto(
      aval_in, manual_axes | set(mesh.manual_axes), mesh)
  return mlir.wrap_with_full_to_shard_op(ctx, sx, aval_out, manual_proto,
                                         unspecified)

