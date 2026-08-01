
def _vector_insert_strided_slice_op_lowering_rule(
    ctx: LoweringContext, op: vector.InsertStridedSliceOp
) -> Sequence[ir.Value]:
  del ctx
  if any(ir.IntegerAttr(s).value != 1 for s in op.strides):
    raise NotImplementedError("`strides` must contain only 1s.")
  [src_layout, dst_layout] = inference_utils.in_layouts(op)
  [out_layout] = inference_utils.out_layouts(op)
  assert src_layout == dst_layout == out_layout
  src = _fragmented_array_from_ir(op.valueToStore, src_layout)
  indices = tuple(
      slice(ir.IntegerAttr(offset).value, ir.IntegerAttr(offset).value + size)
      for offset, size in zip(op.offsets, src.shape, strict=True)
  )
  result = _fragmented_array_from_ir(op.dest, dst_layout)
  result[indices] = src
  assert result.layout == layouts_lib.from_layout_attr(out_layout)
  return [fragmented_array_to_ir(result, op.result.type)]

