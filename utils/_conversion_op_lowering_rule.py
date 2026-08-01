
def _conversion_op_lowering_rule(
    _: LoweringContext,
    op: ir.OpView,
    source_is_signed: bool | None,
    target_is_signed: bool | None,
) -> Sequence[ir.Value]:
  [in_layout] = inference_utils.in_layouts(op)
  [layout] = inference_utils.out_layouts(op)
  if in_layout != layout:
    raise ValueError("Layout mismatch")

  target_ty = op.result.type.element_type
  operand = _fragmented_array_from_ir(op.operands[0], layout, source_is_signed)
  converted = operand.astype(target_ty, is_signed=target_is_signed)
  return [fragmented_array_to_ir(converted, op.result.type)]

