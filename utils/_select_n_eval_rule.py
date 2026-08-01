
def _select_n_eval_rule(ctx: KernelEvalContext, *args):
  return jax.lax.select_n(*args)

