
def _infer_tmem_load_registers_layout(
    tmem_layout: TMEMLayout, columns: int, packing: int
) -> fa.TiledLayout:
  if tmem_layout == tmem_default_layout(packing=packing):
    return LAYOUT
  if tmem_layout == tmem_half_lane_layout(columns, packing=packing):
    return fa.WGMMA_LAYOUT
  if tmem_layout == tmem_m64_collective_layout(columns, packing=packing):
    return fa_m64_collective_layout(columns)
  raise ValueError(f"TMEM layout {tmem_layout} is not supported")

