
def _to_splat_fragmented_layout_attr(
    layout: fa.WGSplatFragLayout,
) -> mgpu.WGSplatFragLayoutAttr:
  """Constructs a #mosaic_gpu.WGSplatFragLayout attribute from a WGSplatFragLayout."""
  shape = ir.DenseI64ArrayAttr.get(layout.shape)
  return mgpu.WGSplatFragLayoutAttr.get(shape)

