
def _bitcast_op_lowering_rule(
    _: LoweringContext, op: arith.BitcastOp
) -> Sequence[ir.Value]:
  in_layouts = inference_utils.in_layouts(op)
  [layout] = inference_utils.out_layouts(op)
  if any(in_layout != layout for in_layout in in_layouts):
    raise ValueError("Layout mismatch")
  in_ = _fragmented_array_from_ir(op.in_, layout)
  out_element_type = ir.VectorType(op.result.type).element_type
  out = in_.bitcast(
      out_element_type,
      output_is_signed=_default_is_signed(out_element_type),
  )
  return [fragmented_array_to_ir(out, op.result.type)]

