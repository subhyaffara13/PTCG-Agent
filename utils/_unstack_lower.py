
def _unstack_lower(ctx, x, *, axis):
  x_aval, = ctx.avals_in

  start_indices = [0] * x_aval.ndim
  limit_indices = list(x_aval.shape)
  strides = (1,) * x_aval.ndim

  slice_shape = list(x_aval.shape)
  slice_shape[axis] = 1
  slice_shape = tuple(slice_shape)

  outs = []
  for aval_out in ctx.avals_out:
    limit_indices[axis] = start_indices[axis] + 1
    slice_out = mlir.slice_op(ctx, x, x_aval.update(shape=slice_shape),
                              start_indices=start_indices,
                              limit_indices=limit_indices, strides=strides)
    squeezed_out = mlir.reshape(ctx, slice_out, aval_out)
    outs.append(mlir.lower_with_sharding_in_types(ctx, squeezed_out, aval_out))

    start_indices[axis] = limit_indices[axis]

  return outs

