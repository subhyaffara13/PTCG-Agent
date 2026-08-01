
def _bitcast_convert_type_eval_rule(eval_ctx: KernelEvalContext, x, new_dtype):
  del eval_ctx
  return jax.lax.bitcast_convert_type(x, new_dtype)

