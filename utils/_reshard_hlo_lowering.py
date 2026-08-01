
def _reshard_hlo_lowering(ctx, x_node, *, dst_sharding, concrete_mesh):
  aval_out, = ctx.avals_out
  return [mlir.lower_with_sharding_in_types(ctx, x_node, aval_out)]

