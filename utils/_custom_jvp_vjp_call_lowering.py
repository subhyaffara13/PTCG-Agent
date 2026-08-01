
def _custom_jvp_vjp_call_lowering(ctx: mlir.LoweringRuleContext, *args,
                                  call_jaxpr: core.ClosedJaxpr, **_):
  consts = mlir.ir_consts(
      call_jaxpr.consts, [v.aval for v in call_jaxpr.jaxpr.constvars])
  out, tokens = mlir.jaxpr_subcomp(ctx.module_context, call_jaxpr.jaxpr,
                                   ctx.name_stack, ctx.tokens_in, consts,
                                   *args, dim_var_values=ctx.dim_var_values,
                                   const_lowering=ctx.const_lowering,
                                   outer_traceback=ctx.traceback)
  ctx.set_tokens_out(tokens)
  return out

