
def _optimization_barrier_lowering(ctx: LoweringRuleContext, *args):
  result = mgpu.optimization_barrier(
      *(_ensure_fa(arg, aval.dtype) for arg, aval in zip(args, ctx.avals_in))
  )
  return (result,) if len(ctx.avals_in) == 1 else result

