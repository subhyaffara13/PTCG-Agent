
def _mgpu_broadcast_in_dim_op_lowering_rule(
    _: LoweringContext, op: mgpu.BroadcastInDimOp
) -> Sequence[ir.Value]:
  out_ty = ir.VectorType(op.result.type)
  broadcast_dims = tuple(op.broadcast_dimensions)
  in_layout_attr = inference_utils.in_layouts(op)[0]
  operand_fa = _fragmented_array_from_ir(op.operand, in_layout_attr)
  out_layout = layouts_lib.from_layout_attr(inference_utils.out_layouts(op)[0])
  out = operand_fa.broadcast_in_dim(
      tuple(out_ty.shape), broadcast_dims, out_layout
  )
  return [fragmented_array_to_ir(out, out_ty)]

