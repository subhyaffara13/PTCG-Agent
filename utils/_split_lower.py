
def _split_lower(ctx, x, *, sizes, axis):
  x_aval, = ctx.avals_in
  start_indices = [0] * x_aval.ndim
  limit_indices = list(x_aval.shape)
  strides = (1,) * x_aval.ndim
  outs = []
  for aval_out in ctx.avals_out:
    limit_indices[axis] = start_indices[axis] + aval_out.shape[axis]
    out = mlir.slice_op(ctx, x, aval_out, start_indices=start_indices,
                        limit_indices=limit_indices, strides=strides)
    outs.append(mlir.lower_with_sharding_in_types(ctx, out, aval_out))
    start_indices[axis] = limit_indices[axis]
  return outs

