
def _random_fold_in_eval_rule(eval_ctx: KernelEvalContext, key, msg):
  del eval_ctx
  return prng.random_fold_in(key, msg)

