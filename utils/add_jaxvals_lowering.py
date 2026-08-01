
def add_jaxvals_lowering(ctx, x, y):
  out_aval, = ctx.avals_out
  if (isinstance(a := ctx.avals_in[0], core.ShapedArray) and
      dtypes.issubdtype(a.dtype, dtypes.extended)):
    return lower_fun(lambda x, y: [a.dtype._rules.add(a.dtype, x, y)])(ctx, x, y)
  out = hlo.add(x, y)
  return [lower_with_sharding_in_types(ctx, out, out_aval)]

