
def _unstack_eval_rule(ctx: KernelEvalContext, x, *, axis):
  return jax.lax.unstack(x, axis=axis)

