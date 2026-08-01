
def _square_lower_hlo(ctx, x):
  if dtypes.issubdtype(ctx.avals_in[0].dtype, np.integer):
    return [hlo.multiply(x, x)]
  return [chlo.square(x)]

