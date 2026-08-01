
def _eltwise_usage_rule(
    prim: core.Primitive, ctx: UsageRuleContext, used_out: set[Usage], **params
) -> Sequence[set[Usage]]:
  del ctx, prim, params
  return [used_out]

