
def _reduce_and_lowering_rule(ctx: LoweringRuleContext, x, *, axes):
  def _proxy_reduce(arg, *, axes):
    # Mosaic currently only supports float reductions, so we cast the boolean
    # arg to a float and use reduce_min to implement reduce_and.
    # TODO(b/351017807): Implement this logic in Mosaic MultiDimReductionOp
    # instead.
    float_arg = jnp.where(arg, 1.0, 0.0)
    return jnp.min(float_arg, axis=axes) > 0.0
  proxy_lowering = lower_fun(_proxy_reduce)
  return proxy_lowering(ctx, x, axes=axes)

