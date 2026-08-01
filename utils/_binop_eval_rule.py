
def _binop_eval_rule(prim, ctx, x, y, **params):
  del ctx
  return prim.bind(x, y, **params)

