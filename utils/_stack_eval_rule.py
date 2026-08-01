
def _stack_eval_rule(ctx: KernelEvalContext, *args, axis):
  return jax.lax.stack(args, axis=axis)

