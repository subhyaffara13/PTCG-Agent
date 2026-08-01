
def _slice_lower(ctx, x, *, start_indices, limit_indices, strides):
  strides = strides or [1] * len(start_indices)
  aval_out, = ctx.avals_out
  out = mlir.slice_op(ctx, x, aval_out, start_indices=start_indices,
                      limit_indices=limit_indices, strides=strides)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

