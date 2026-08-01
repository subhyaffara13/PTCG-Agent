
def _sin_lowering(ctx, x, accuracy):
  if dtypes.issubdtype(ctx.avals_in[0].dtype, np.complexfloating):
    sine = mlir.lower_fun(_sin_complex, multiple_results=False)
    return sine(ctx, x)
  return _nary_lower_hlo(hlo.sine, ctx, x, accuracy=accuracy)

