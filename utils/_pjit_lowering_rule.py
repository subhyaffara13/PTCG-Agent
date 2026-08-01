
def _pjit_lowering_rule(ctx: LoweringRuleContext, *args, jaxpr, **_):
  lowering_context = ctx.lowering_context.replace(block_shapes=ctx.block_shapes)
  return jaxpr_subcomp(lowering_context, jaxpr.jaxpr, *args)


def _pjit_lowering_rule(ctx: LoweringRuleContext, *args, jaxpr, **kwargs):
  if jaxpr.consts:
    raise NotImplementedError
  return lower_jaxpr_to_mosaic_gpu(
      ctx.module_ctx, ctx.launch_ctx, jaxpr.jaxpr, args,
  )


def _pjit_lowering_rule(ctx: LoweringRuleContext, *args, jaxpr, **_):
  if jaxpr.consts:
    raise NotImplementedError
  return lower_jaxpr_to_triton_ir(
      ctx.context, jaxpr.jaxpr, ctx.block_infos, *args
  )

