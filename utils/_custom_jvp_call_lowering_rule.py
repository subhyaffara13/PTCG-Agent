
def _custom_jvp_call_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    call_jaxpr: jax_core.ClosedJaxpr,
    jvp_jaxpr_fun: lu.WrappedFun,
    num_consts: int,
    symbolic_zeros: bool,
):
  del jvp_jaxpr_fun
  if symbolic_zeros: raise NotImplementedError
  if num_consts: raise NotImplementedError
  if call_jaxpr.consts: raise NotImplementedError
  lowering_context = ctx.lowering_context.replace(block_shapes=ctx.block_shapes)
  return jaxpr_subcomp(lowering_context, call_jaxpr.jaxpr, *args)

