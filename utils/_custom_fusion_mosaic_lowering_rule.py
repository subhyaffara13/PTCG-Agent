
def _custom_fusion_mosaic_lowering_rule(
    ctx: mosaic_lowering.LoweringRuleContext,
    *args,
    jaxpr: core.Jaxpr,
    num_consts: int,
    pallas_jaxpr: core.Jaxpr | None,
    pallas_num_consts: int,
    **_):
  consts, pallas_consts, args = util.split_list(
      args, [num_consts, pallas_num_consts])
  if pallas_jaxpr is None:
    pallas_jaxpr = jaxpr
    pallas_consts = consts
  lowering_context = ctx.lowering_context.replace(block_shapes=ctx.block_shapes)
  return mosaic_lowering.jaxpr_subcomp(
      lowering_context, pallas_jaxpr, *pallas_consts, *args)

