
def _concatenate_lower(ctx, *xs, dimension):
  aval_out, = ctx.avals_out
  out = _concatenate_tree(xs, dimension)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

