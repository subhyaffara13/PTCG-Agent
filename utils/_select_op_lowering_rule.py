
def _select_op_lowering_rule(
    ctx: LoweringContext, op: arith.SelectOp
) -> Sequence[ir.Value]:
  del ctx
  in_layouts = inference_utils.in_layouts(op)
  [layout] = inference_utils.out_layouts(op)
  if any(in_layout != layout for in_layout in in_layouts):
    raise ValueError("Layout mismatch")
  pred = _fragmented_array_from_ir(op.condition, layout)
  true_value = _fragmented_array_from_ir(op.true_value, layout)
  false_value = _fragmented_array_from_ir(op.false_value, layout)
  result = pred.select(true_value, false_value)
  return [fragmented_array_to_ir(result, op.result.type)]

