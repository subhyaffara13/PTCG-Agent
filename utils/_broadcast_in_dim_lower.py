
def _broadcast_in_dim_lower(ctx, x, shape, broadcast_dimensions,
                            sharding) -> Sequence[ir.Value]:
  aval_out, = ctx.avals_out
  out = mlir.broadcast_in_dim(ctx, x, aval_out,
                              broadcast_dimensions=broadcast_dimensions)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

