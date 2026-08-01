
def _get_barrier_semaphore_rule(ctx: LoweringRuleContext):
  memref_type = ctx.aval_to_ir_type(ctx.avals_out[0])
  return tpu.sem_barrier(memref_type)

