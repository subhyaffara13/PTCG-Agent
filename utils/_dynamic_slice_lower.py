
def _dynamic_slice_lower(ctx, x, *start_indices, slice_sizes):
  x_aval, *_ = ctx.avals_in
  aval_out, = ctx.avals_out
  out = mlir.dynamic_slice(ctx, aval_out, x, start_indices=start_indices)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

