
def _dot_general_eval_rule(ctx: KernelEvalContext, x, y, **params):
  del ctx
  return lax.dot_general_p.bind(x, y, **params)

