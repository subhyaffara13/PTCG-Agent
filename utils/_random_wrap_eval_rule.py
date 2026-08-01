
def _random_wrap_eval_rule(eval_ctx: KernelEvalContext, arr, *, impl):
  del eval_ctx
  return jax.random.wrap_key_data(arr, impl=impl)

