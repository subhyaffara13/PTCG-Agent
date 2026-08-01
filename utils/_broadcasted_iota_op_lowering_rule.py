
def _broadcasted_iota_op_lowering_rule(
    ctx: LoweringContext, op: mgpu.BroadcastedIotaOp
) -> Sequence[ir.Value]:
  del ctx
  [layout] = inference_utils.out_layouts(op)
  result_type = ir.VectorType(op.result.type)
  a = fa.FragmentedArray.broadcasted_iota(
      result_type.element_type,
      tuple(result_type.shape),
      op.dimension.value,
      layouts_lib.from_layout_attr(layout),
      is_signed=_default_is_signed(result_type.element_type),
  )
  return [fragmented_array_to_ir(a, result_type)]

