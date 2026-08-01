
def _eltwise_eval_rule(prim, ctx, x, **params):
  del ctx
  return prim.bind(x, **params)

