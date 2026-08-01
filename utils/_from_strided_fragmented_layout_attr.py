
def _from_strided_fragmented_layout_attr(
    attr: mgpu.WGStridedFragLayoutAttr,
) -> fa.WGStridedFragLayout:
  """Constructs a WGStridedFragLayout from a #mosaic_gpu.WGStridedFragLayout attribute."""
  return fa.WGStridedFragLayout(
      shape=tuple(attr.shape), vec_size=attr.vector_size
  )

