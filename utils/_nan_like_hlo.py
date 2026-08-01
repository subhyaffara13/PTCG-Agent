
def _nan_like_hlo(ctx: mlir.LoweringRuleContext, aval) -> ir.Value:
  if dtypes.issubdtype(aval.dtype, np.complexfloating):
    return mlir.full_like_aval(ctx, np.nan + np.nan * 1j, aval)
  else:
    return mlir.full_like_aval(ctx, np.nan, aval)

