
def _compare_lower_hlo(direction: str, total_order: bool, ctx, x, y):
  avals_in, (aval_out,) = ctx.avals_in, ctx.avals_out
  x_dtype = avals_in[0].dtype
  x, y = mlir.multi_broadcast_in_dim(ctx, (x, y), avals_in, aval_out.shape,
                                     aval_out.sharding)
  if dtypes.issubdtype(x_dtype, dtypes.extended):
    assert not total_order
    return _compare_lower_hlo_opaque(direction, ctx, avals_in, aval_out, x, y)
  if dtypes.issubdtype(x_dtype, np.inexact):
    compare_type = "TOTALORDER" if total_order else "FLOAT"
  elif dtypes.issubdtype(x_dtype, np.signedinteger):
    compare_type = "SIGNED"
  else:
    compare_type = "UNSIGNED"
  return [mlir.compare_hlo(x, y, direction, compare_type)]

