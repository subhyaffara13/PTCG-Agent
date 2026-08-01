
def _remat_lowering_rule(ctx: LoweringRuleContext, *args, jaxpr, **_):
  return lower_jaxpr_to_triton_ir(ctx.context, jaxpr, ctx.block_infos, *args)

