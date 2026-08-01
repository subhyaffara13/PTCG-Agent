
def _cholesky_lowering(ctx, x):
  del ctx  # unused
  return [hlo.cholesky(x, lower=ir.BoolAttr.get(True))]

