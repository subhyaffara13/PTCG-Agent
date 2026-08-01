
def _to_strided_fragmented_layout_attr(
    layout: fa.WGStridedFragLayout,
) -> mgpu.WGStridedFragLayoutAttr:
  """Constructs a #mosaic_gpu.WGStridedFragLayout attribute from a WGStridedFragLayout."""
  shape = ir.DenseI64ArrayAttr.get(layout.shape)
  return mgpu.WGStridedFragLayoutAttr.get(shape, layout.vec_size)

