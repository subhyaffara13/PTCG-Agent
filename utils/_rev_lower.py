
def _rev_lower(ctx, x, *, dimensions):
  aval_out, = ctx.avals_out
  out = hlo.reverse(x, mlir.dense_int_array(dimensions))
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

