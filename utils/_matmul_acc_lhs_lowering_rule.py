
def _matmul_acc_lhs_lowering_rule(
    ctx: LoweringRuleContext,
    lhs: ir.Value,
    *,
    acc_addr: int,
    mxu_index: int,
    load_staged_rhs: int | None,
):
  del ctx
  staged_rhs_kwarg: dict[str, Any] = {}
  if load_staged_rhs is not None:
    staged_rhs_kwarg = {"load_staged_rhs": load_staged_rhs}
  tpu.matmul_acc_lhs(acc_addr, lhs, mxu_index, **staged_rhs_kwarg)
  return []

