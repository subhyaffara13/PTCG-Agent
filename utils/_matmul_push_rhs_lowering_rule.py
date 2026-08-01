
def _matmul_push_rhs_lowering_rule(
    ctx: LoweringRuleContext,
    rhs: ir.Value,
    *,
    staging_register: int,
    mxu_index: int,
    transpose: bool = False,
):
  del ctx
  tpu.matmul_push_rhs(
      rhs, mxu_index, staging_register=staging_register, transpose=transpose
  )
  return []

