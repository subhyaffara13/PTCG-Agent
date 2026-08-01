
def _from_splat_fragmented_layout_attr(
    attr: mgpu.WGSplatFragLayoutAttr,
) -> fa.WGSplatFragLayout:
  return fa.WGSplatFragLayout(shape=tuple(attr.shape))

