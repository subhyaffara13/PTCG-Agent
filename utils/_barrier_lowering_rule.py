
def _barrier_lowering_rule(ctx: sc_lowering.LoweringRuleContext):
  ix = ir.IndexType.get()
  tpu.barrier(arith.constant(ix, ir.IntegerAttr.get(ix, 0)))
  return ()

