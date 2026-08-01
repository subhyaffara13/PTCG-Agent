
def _cmpi_op_lowering_rule(
    _: LoweringContext, op: arith.CmpIOp
) -> Sequence[ir.Value]:
  in_layouts = inference_utils.in_layouts(op)
  [layout] = inference_utils.out_layouts(op)
  if any(in_layout != layout for in_layout in in_layouts):
    raise ValueError("Layout mismatch")
  # pyrefly: ignore[missing-attribute]
  impl, is_signed = CMPI_IMPLS[op.predicate.value]
  lhs = _fragmented_array_from_ir(op.lhs, layout, is_signed)
  rhs = _fragmented_array_from_ir(op.rhs, layout, is_signed)
  return [fragmented_array_to_ir(impl(lhs, rhs), op.result.type)]

