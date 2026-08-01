
def _iota_lower(ctx, dtype, shape, dimension, sharding):
  del dtype
  aval_out, = ctx.avals_out
  out = mlir.iota(ctx, aval_out, dimension=dimension)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

