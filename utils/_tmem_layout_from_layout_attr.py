
def _tmem_layout_from_layout_attr(
    layout_attr: ir.Attribute,
) -> tcgen05.TMEMLayout:
  layout = layouts_lib.from_layout_attr(layout_attr)
  assert isinstance(layout, fa.TiledLayout)
  return tcgen05.TMEMLayout(
      layout.tiling, layout.warp_dims, layout.lane_dims, layout.vector_dim
  )

