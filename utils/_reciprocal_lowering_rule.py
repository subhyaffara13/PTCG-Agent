
def _reciprocal_lowering_rule(
    ctx: mlir.LoweringRuleContext,
    x,
    *,
    approx=False,
    full_range=True,
):
  del full_range

  def _reciprocal(x, *, approx=False):
    if approx:
      return jnp.reciprocal(x.astype(jnp.bfloat16)).astype(jnp.float32)
    return jnp.reciprocal(x)

  return mlir.lower_fun(_reciprocal, multiple_results=False)(
      ctx, x, approx=approx
  )


def _reciprocal_lowering_rule(
    ctx: LoweringRuleContext, x, *, approx, full_range
):
  if not isinstance(x.type.element_type, ir.F32Type):
    raise ValueError("Only float32 is supported.")
  if (
      TYPE_CHECKING
      or ctx.forward_compatible
  ):
    return tpu.reciprocal(x, approx=approx)
  else:
    return tpu.reciprocal(x, approx=approx, full_range=full_range)

