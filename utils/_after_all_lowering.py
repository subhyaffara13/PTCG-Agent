
def _after_all_lowering(ctx, *operands):
  aval_out, = ctx.avals_out
  return [hlo.after_all(operands)]

