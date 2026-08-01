
def _tile_lower(ctx, x, reps) -> Sequence[ir.Value]:
  aval_out, = ctx.avals_out
  x_aval, = ctx.avals_in
  expand_shape = tuple(j for i in x_aval.shape for j in [1, i])
  expand_sharding = NamedSharding(
      x_aval.sharding.mesh.abstract_mesh,
      P(*tuple(s for d in x_aval.sharding.spec for s in [None, d])),
  )
  reshaped_aval = x_aval.update(shape=expand_shape, sharding=expand_sharding)
  reshaped = mlir.reshape(ctx, x, reshaped_aval)
  reshaped = mlir.lower_with_sharding_in_types(ctx, reshaped, reshaped_aval)
  broadcast_shape = tuple(k for pair in zip(reps, x_aval.shape) for k in pair)
  broadcasted_aval = x_aval.update(
      shape=broadcast_shape, sharding=expand_sharding)
  broadcasted = mlir.broadcast_in_dim(ctx, reshaped,
      broadcasted_aval, broadcast_dimensions=tuple(range(2 * x_aval.ndim)))
  broadcasted = mlir.lower_with_sharding_in_types(
      ctx, broadcasted, broadcasted_aval)
  out = mlir.reshape(ctx, broadcasted, aval_out)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

