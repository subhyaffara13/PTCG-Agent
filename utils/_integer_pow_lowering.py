
def _integer_pow_lowering(ctx, x, *, y):
  # These cases are subsumed by the general case, but it's faster to emit these
  # common cases directly.
  if y == 1:
    out = x
  elif y == 2:
    out = hlo.multiply(x, x)
  elif y == 3:
    out = hlo.multiply(hlo.multiply(x, x), x)
  elif y == -1:
    out = hlo.divide(mlir.full_like_aval(ctx, 1, ctx.avals_in[0]), x)
  else:
    lowering = mlir.lower_fun(_integer_pow, multiple_results=False)
    out, = lowering(ctx, x, y=y)
  aval_out, = ctx.avals_out
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

