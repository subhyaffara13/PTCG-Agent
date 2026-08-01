
def _squeeze_lower(ctx, operand, *, dimensions):
  del dimensions  # Implied by the output aval.
  aval_out, = ctx.avals_out
  out = mlir.reshape(ctx, operand, aval_out)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

