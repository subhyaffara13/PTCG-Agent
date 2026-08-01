
def _create_token_lowering(ctx, *operands):
  aval_out, = ctx.avals_out
  return [hlo.create_token()]

