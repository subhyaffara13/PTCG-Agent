
def _reshape_lower(ctx, x, new_sizes, dimensions, sharding):
  aval_out, = ctx.avals_out
  if dimensions is not None:
    x = hlo.transpose(x, mlir.dense_int_array(dimensions))
  out = mlir.reshape(ctx, x, aval_out)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

