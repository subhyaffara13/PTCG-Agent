
def _shape_assertion_lowering_rule(ctx: mlir.LoweringRuleContext,
                                   assert_what: mlir.ir.Value,
                                   *error_message_inputs: mlir.ir.Value,
                                   error_message: str):
  op = mlir.custom_call(
    "shape_assertion",
    result_types=[],  # No results
    operands=[assert_what, *error_message_inputs],
    has_side_effect=True,
    extra_attributes=dict(error_message=mlir.ir.StringAttr.get(error_message))
  )
  return op.results

