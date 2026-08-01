
def _vector_extract_op_lowering_rule(
    ctx: LoweringContext, op: vector.ExtractOp
) -> Sequence[ir.Value]:
  del ctx
  if op.dynamic_position:
    raise NotImplementedError("Only slicing with static indices allowed.")

  [in_layout] = inference_utils.in_layouts(op)
  a = _fragmented_array_from_ir(op.source, in_layout)

  if not isinstance(op.result.type, ir.VectorType):  # scalar result
    result = a[tuple(op.static_position)]
    assert isinstance(result.layout, fa.WGSplatFragLayout)
    return [result.registers.item()]

  [out_layout] = inference_utils.out_layouts(op)
  assert in_layout == out_layout
  a = _fragmented_array_from_ir(op.source, in_layout)
  result_type = ir.VectorType(op.result.type)
  slices = tuple(slice(i, i + 1) for i in op.static_position)
  # TODO(allanrenucci): Add direct support for indexing to FragmentedArray.
  result = a[slices].reshape(tuple(result_type.shape))
  assert result.layout == layouts_lib.from_layout_attr(out_layout)
  return [fragmented_array_to_ir(result, result_type)]

