
def _convert_element_type_eval_rule(
    eval_ctx: KernelEvalContext, x, new_dtype, **params
):
  del eval_ctx, params
  return jax.lax.convert_element_type(x, new_dtype)

