
def _vector_multi_dim_reduction_op_lowering_rule(
    ctx: LoweringContext, op: vector.MultiDimReductionOp
) -> Sequence[ir.Value]:
  [in_layout, acc_layout] = inference_utils.in_layouts(op)
  [out_layout] = inference_utils.out_layouts(op)
  if out_layout != acc_layout:
    raise ValueError(
        f"Output layout {out_layout} must match the accumulator layout"
        f" {acc_layout}"
    )

  if len(op.reduction_dims) != 1:
    raise NotImplementedError("Only 1 reduction dimension is supported.")

  op_kind = _combining_kind(op.kind)
  is_signed = _is_reduction_signed(op_kind)
  src = _fragmented_array_from_ir(op.source, in_layout, is_signed)
  acc = _fragmented_array_from_ir(op.acc, acc_layout, is_signed)

  if not isinstance(src.layout, fa.TiledLayout):
    raise NotImplementedError(f"Unsupported layout: {src.layout}")
  reduced_dim = src.layout.tiling.tile_dimension(op.reduction_dims[0])
  if any(reduced_dim[d] for d in src.layout.partitioned_warp_dims):
    # cross-warp reductions require scratch space.
    dtype = op.source.type.element_type
    allocation_size = ir.IntegerAttr(op.attributes["scratch_size"]).value * 8 // utils.bitwidth(dtype)
    scratch = _slice_smem(
        ir.MemRefType.get([allocation_size], dtype, memory_space=utils.smem()),
        ir.IntegerAttr(op.attributes["offset"]).value,
        ctx.smem_requested_bytes,
    )
  else:
    scratch = None

  match op_kind:
    case vector.CombiningKind.ADD:
      result = src.reduce("add", op.reduction_dims[0], scratch)
      result += acc
    case vector.CombiningKind.MAXSI | vector.CombiningKind.MAXUI | vector.CombiningKind.MAXIMUMF:
      result = src.reduce("max", op.reduction_dims[0], scratch)
      result = result.max(acc)
    case vector.CombiningKind.MINUI | vector.CombiningKind.MINSI | vector.CombiningKind.MINIMUMF:
      result = src.reduce("min", op.reduction_dims[0], scratch)
      result = result.min(acc)
    case _:
      raise NotImplementedError(f"Unsupported reduction kind: {op.kind}")
  assert result.layout == layouts_lib.from_layout_attr(out_layout)
  return [fragmented_array_to_ir(result, op.result.type)]

