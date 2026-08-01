
def _mgpu_layout_cast_op_lowering_rule(
    _: LoweringContext, op: mgpu.LayoutCastOp
) -> Sequence[ir.Value]:
  [in_layout] = inference_utils.in_layouts(op)
  [out_layout] = inference_utils.out_layouts(op)
  in_array = _fragmented_array_from_ir(op.x, in_layout)
  out_array = in_array.to_layout(layouts_lib.from_layout_attr(out_layout))
  return [fragmented_array_to_ir(out_array, op.result.type)]

