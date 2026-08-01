
def _closed_call_lowering_rule(ctx, *args, call_jaxpr: jax_core.ClosedJaxpr):
  if call_jaxpr.consts: raise NotImplementedError
  return lowering.lower_jaxpr_to_mosaic_gpu(
      ctx.module_ctx, ctx.launch_ctx, call_jaxpr.jaxpr, args)


def _closed_call_lowering_rule(
    ctx: LoweringRuleContext, *args, call_jaxpr, **_
):
  jaxpr, consts = call_jaxpr.jaxpr, call_jaxpr.consts
  if consts:
    raise NotImplementedError
  return lower_jaxpr_to_triton_ir(ctx.context, jaxpr, ctx.block_infos, *args)

