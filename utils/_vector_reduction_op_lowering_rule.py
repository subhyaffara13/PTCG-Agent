
def _vector_reduction_op_lowering_rule(
    ctx: LoweringContext, op: vector.ReductionOp
) -> Sequence[ir.Value]:
  [layout] = inference_utils.in_layouts(op)
  element_type = op.vector.type.element_type
  scratch = _slice_smem(
      ir.MemRefType.get([4], element_type, memory_space=utils.smem()),
      ir.IntegerAttr(op.attributes["offset"]).value,
      ctx.smem_requested_bytes,
  )
  axes = range(op.vector.type.rank)
  op_kind = _combining_kind(op.kind)
  is_signed = _is_reduction_signed(op_kind)
  a = _fragmented_array_from_ir(op.vector, layout, is_signed)
  match op_kind:
    case vector.CombiningKind.ADD:
      result = a.reduce("add", axes, scratch)
    case vector.CombiningKind.MAXSI | vector.CombiningKind.MAXUI | vector.CombiningKind.MAXIMUMF:
      result = a.reduce("max", axes, scratch)
    case vector.CombiningKind.MINUI | vector.CombiningKind.MINSI | vector.CombiningKind.MINIMUMF:
      result = a.reduce("min", axes, scratch)
    case _:
      raise NotImplementedError(f"Unsupported reduction kind: {op.kind}")
  assert isinstance(result.layout, fa.WGSplatFragLayout)
  return [result.registers.item()]

