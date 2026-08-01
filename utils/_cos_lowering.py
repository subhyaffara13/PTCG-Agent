
def _cos_lowering(ctx, x, accuracy):
  if dtypes.issubdtype(ctx.avals_in[0].dtype, np.complexfloating):
    cosine = mlir.lower_fun(_cos_complex, multiple_results=False)
    return cosine(ctx, x)
  return _nary_lower_hlo(hlo.cosine, ctx, x, accuracy=accuracy)

