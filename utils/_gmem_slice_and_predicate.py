
def _gmem_slice_and_predicate(
    ctx: LoweringContext,
    op: mgpu.AsyncLoadOp | mgpu.AsyncPrefetchOp | mgpu.AsyncStoreOp,
) -> tuple[
    tuple[ir.Value | fa.FragmentedArray | utils.DynamicSlice, ...],
    dict[str, ir.Value],
]:
  """Returns the GMEM slice and predicate for the given async op."""
  gmem_slice: list[ir.Value | fa.FragmentedArray | utils.DynamicSlice]
  gmem_slice = []
  predicate = dict(predicate=ctx.single_lane_predicate)
  for idx, size in zip(op.indices, op.slice_lengths, strict=True):
    if isinstance(idx.type, ir.IntegerType):
      idx_int = arith.index_cast(ir.IndexType.get(), idx)
      v = idx_int if size < 0 else utils.DynamicSlice(idx_int, size)
      gmem_slice.append(v)
    elif isinstance(idx.type, ir.VectorType):
      layout = inference_utils.in_layouts(op)[0]
      assert layouts_lib.from_layout_attr(layout) in (fa.TMA_INDICES_LAYOUT, fa.TMA_INDICES_4_LAYOUT), layout
      idx_fa = _fragmented_array_from_ir(idx, layout)
      gmem_slice.append(idx_fa)
      predicate = dict()
    else:
      raise TypeError(f"Unsupported index type: {idx.type}")
  return tuple(gmem_slice), predicate

