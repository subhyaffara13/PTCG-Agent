
def _custom_vjp_call_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    call_jaxpr,
    fwd_jaxpr_thunk,
    out_trees,
    symbolic_zeros,
    bwd,
    num_consts,
):
  if num_consts: raise NotImplementedError
  lowering_context = ctx.lowering_context.replace(block_shapes=ctx.block_shapes)
  return jaxpr_subcomp(lowering_context, call_jaxpr.jaxpr, *args)

