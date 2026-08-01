
def _squeeze_eval_rule(ctx: KernelEvalContext, x: jax.Array, **params: Any):
  del ctx, params
  return x

