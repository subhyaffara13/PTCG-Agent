
def _traverse_op_lowering_rule(
    ctx: LoweringContext, op: ir.OpView
) -> MlirLoweringRuleResult:
  if inference_utils.should_have_layout(op):
    raise ValueError(
        f"Rule cannot handle an op with vector operands or results: {op}"
    )
  for region in op.operation.regions:
    for block in region:
      for block_op in list(block):
        with ir.InsertionPoint(block_op):
          ctx.lower_op(block_op)
  return RECURSED

