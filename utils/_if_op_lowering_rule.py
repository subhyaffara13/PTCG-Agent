
def _if_op_lowering_rule(
    ctx: LoweringContext, if_op: scf.IfOp
) -> MlirLoweringRuleResult:
  if not inference_utils.should_have_layout(if_op):
    return _traverse_op_lowering_rule(ctx, if_op)

  raise NotImplementedError

