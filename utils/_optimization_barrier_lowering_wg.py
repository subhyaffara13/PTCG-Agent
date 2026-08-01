
def _optimization_barrier_lowering_wg(ctx: LoweringRuleContext, *args):
  result = mgpu.dialect.optimization_barrier([
      _ensure_ir_value(arg, aval.dtype) for arg, aval in zip(args, ctx.avals_in)
  ])
  return (result,) if len(ctx.avals_in) == 1 else result

