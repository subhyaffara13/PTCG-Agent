
def _sign_lower_hlo(ctx, x):
  x_aval, = ctx.avals_in
  if dtypes.issubdtype(x_aval.dtype, np.unsignedinteger):
    return [hlo.select(
        mlir.compare_hlo(x, mlir.full_like_aval(ctx, 0, x_aval), 'EQ',
                         'UNSIGNED'),
        mlir.full_like_aval(ctx, 0, x_aval),
        mlir.full_like_aval(ctx, 1, x_aval))]
  return [hlo.sign(x)]

