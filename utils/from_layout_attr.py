
def from_layout_attr(attr: ir.Attribute) -> fa.FragmentedLayout:
  """Constructs a layout from an MLIR attribute."""
  if isinstance(attr, mgpu.WGSplatFragLayoutAttr):
    return _from_splat_fragmented_layout_attr(attr)
  elif isinstance(attr, mgpu.WGStridedFragLayoutAttr):
    return _from_strided_fragmented_layout_attr(attr)
  elif isinstance(attr, mgpu.TiledLayoutAttr):
    return _from_tiled_layout_attr(attr)
  else:
    raise NotImplementedError(
        f"Unsupported layout for conversion from MLIR attribute: {attr}"
    )

