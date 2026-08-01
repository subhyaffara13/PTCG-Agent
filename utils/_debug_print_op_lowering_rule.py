
def _debug_print_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.DebugPrintOp
) -> Sequence[ir.Value]:
  del ctx
  [layout] = inference_utils.in_layouts(op)
  a = _fragmented_array_from_ir(op.value, layout)
  a.debug_print(op.format.value)
  return []

