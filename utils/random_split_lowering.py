
def random_split_lowering(ctx, keys, *, shape):
  aval, = ctx.avals_in
  impl = aval.dtype._impl
  split = iterated_vmap_unary(aval.ndim, lambda k: impl.split(k, shape))
  split_lowering = mlir.lower_fun(split, multiple_results=False)
  return mlir.delegate_lowering(
      ctx, split_lowering, keys,
      avals_in=[core.physical_aval(aval)],
      avals_out=map(core.physical_aval, ctx.avals_out))

