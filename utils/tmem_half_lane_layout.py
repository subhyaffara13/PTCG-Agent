
def tmem_half_lane_layout(columns, packing: int = 1) -> TMEMLayout:
  """A TMEM layout used for 1CTA MMA with M=64."""
  if packing > (columns // 2) or packing.bit_count() != 1:
    raise ValueError(f"Packing must be <= 8 and a power of 2, got: {packing}")
  if columns % 16:
    raise ValueError(f"Columns must be a multiple of 16, got: {columns}")
  return TMEMLayout(
      fa.Tiling((
          (TMEM_ROWS // 2, columns),
          (fa.WARP_SIZE // 2, columns // 2),
          (packing,),
      )),
      warp_dims=(-5,),
      lane_dims=(-4, -3),
      vector_dim=-1,
  )

