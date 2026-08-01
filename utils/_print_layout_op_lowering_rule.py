
def _print_layout_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.PrintLayoutOp
) -> Sequence[ir.Value]:
  del ctx
  if isinstance(op.value.type, ir.VectorType):
    (layout,) = inference_utils.in_layouts(op)
    a = _fragmented_array_from_ir(op.value, layout)
    print(op.format.value.format(pprint_layout(a)))
  else:
    (layout,) = inference_utils.in_tmem_layouts(op)
    ref = _tmem_ref_from_ir(op.value, layout)
    print(op.format.value.format(pprint_layout(ref)))
  return []

