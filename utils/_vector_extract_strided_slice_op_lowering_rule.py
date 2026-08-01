
def _vector_extract_strided_slice_op_lowering_rule(
    ctx: LoweringContext, op: vector.ExtractStridedSliceOp
) -> Sequence[ir.Value]:
  del ctx
  if any(ir.IntegerAttr(s).value != 1 for s in op.strides):
    raise NotImplementedError("`strides` must contain only 1s.")
  [in_layout] = inference_utils.in_layouts(op)
  [out_layout] = inference_utils.out_layouts(op)
  assert in_layout == out_layout
  out_vec_ty = ir.VectorType(op.result.type)
  assert out_vec_ty.has_static_shape
  a = _fragmented_array_from_ir(op.source, in_layout)
  indices = tuple(
      utils.DynamicSlice(
          ir.IntegerAttr(offset).value, ir.IntegerAttr(length).value
      )
      for offset, length in zip(op.offsets, op.sizes, strict=True)
  )
  result = a[indices]
  assert result.layout == layouts_lib.from_layout_attr(out_layout)
  return [fragmented_array_to_ir(result, out_vec_ty)]

