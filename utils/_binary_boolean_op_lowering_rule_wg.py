
def _binary_boolean_op_lowering_rule_wg(
    ctx: LoweringRuleContext, x, y, *, impl
):
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    if any(aval_in.shape for aval_in in ctx.avals_in):
      raise NotImplementedError(
          "Non-scalar arithmetic is not supported in warp-level lowering.")
  x, y = _bcast_wg(x, y, *ctx.avals_in, *ctx.avals_out)
  return impl(x, y)

