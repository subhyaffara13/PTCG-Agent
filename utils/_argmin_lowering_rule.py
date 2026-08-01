
def _argmin_lowering_rule(ctx: LoweringRuleContext, x, axes, index_dtype):
  return _reduce_index_helper(
      ctx, x, axes, index_dtype,
      ir.Attribute.parse("#tpu.reduction_kind<arg_min>")
  )

