
def _vector_broadcast_op_lowering_rule(
    _: LoweringContext, op: vector.BroadcastOp
) -> Sequence[ir.Value]:
  out_vec_ty = ir.VectorType(op.vector.type)
  fragmented_array = fa.FragmentedArray.splat(
      op.source,
      tuple(out_vec_ty.shape),
      layouts_lib.from_layout_attr(inference_utils.out_layouts(op)[0]),
      is_signed=_default_is_signed(out_vec_ty.element_type),
  )
  return [fragmented_array_to_ir(fragmented_array, out_vec_ty)]

