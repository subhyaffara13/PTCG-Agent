
def _optimization_barrier_op_lowering_rule(
    _: LoweringContext,
    op: mgpu.OptimizationBarrierOp,
) -> Sequence[ir.Value]:
  if not all(
      isinstance(operand.type, ir.VectorType) for operand in op.operands
  ):
    raise NotImplementedError(
        f"Optimization barrier op {op} has non-vector operands."
    )

  fragmented_arrays = []
  for operand, layout in zip(op.operands, inference_utils.in_layouts(op), strict=True):
    fragmented_arrays.append(_fragmented_array_from_ir(operand, layout))

  lowered_fragmented_arrays = fa.optimization_barrier(*fragmented_arrays)
  if isinstance(lowered_fragmented_arrays, fa.FragmentedArray):
    lowered_fragmented_arrays = [lowered_fragmented_arrays]

  return [
      fragmented_array_to_ir(arr, result.type)
      for arr, result in zip(lowered_fragmented_arrays, op.results, strict=True)
  ]

