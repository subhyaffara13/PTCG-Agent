
def _custom_call_hi_primitive_eval_rule(
    ctx: KernelEvalContext, *args, _prim
):
  return jax.tree.leaves(_prim.block_eval_rule(ctx, *args))

