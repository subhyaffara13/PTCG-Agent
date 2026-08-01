
def core_call_lowering(ctx: LoweringRuleContext,
                       *args, name, backend=None,
                       call_jaxpr: core.ClosedJaxpr | core.Jaxpr):
  if isinstance(call_jaxpr, core.Jaxpr):
    call_jaxpr = pe.close_jaxpr(call_jaxpr)
  effects = list(effects_lib.ordered_effects.filter_in(call_jaxpr.effects))
  tokens_in = ctx.tokens_in.subset(effects)
  out_nodes, tokens = call_lowering(
      name, call_jaxpr, backend, ctx.module_context,
      ctx.avals_in, ctx.avals_out, tokens_in, *args,
      dim_var_values=ctx.dim_var_values,
      const_lowering=ctx.const_lowering)
  ctx.set_tokens_out(ctx.tokens_in.update_tokens(tokens))
  return out_nodes

