
def _stack_lower(ctx, *xs, axis):
  x_aval = ctx.avals_in[0]
  aval_out, = ctx.avals_out
  ndim = x_aval.ndim

  new_shape = list(x_aval.shape)
  new_shape.insert(axis, 1)

  broadcast_dimensions = [i for i in range(ndim + 1) if i != axis]

  out_sharding = aval_out.sharding
  expanded_xs = []
  for x, aval in zip(xs, ctx.avals_in):
    expanded_aval = aval.update(shape=new_shape, sharding=out_sharding)
    expanded_x = mlir.broadcast_in_dim(
        ctx, x, expanded_aval, broadcast_dimensions=broadcast_dimensions)
    expanded_xs.append(expanded_x)

  out = _concatenate_tree(expanded_xs, axis)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

