
def _pow_lower(ctx, x, y):
  x_aval, y_aval = ctx.avals_in
  if x_aval.dtype != y_aval.dtype:
    out_aval, = ctx.avals_out
    y_aval = y_aval.update(dtype=out_aval.dtype)
    y = hlo.convert(mlir.aval_to_ir_type(ctx.module_context, y_aval), y)
    ctx = ctx.replace(avals_in=[x_aval, y_aval])
  return _nary_lower_hlo(hlo.power, ctx, x, y)

