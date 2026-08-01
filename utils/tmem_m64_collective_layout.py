
def tmem_m64_collective_layout(columns: int, packing: int = 1) -> TMEMLayout:
  """A TMEM layout used for 2CTA MMA with M=128."""
  if packing > 8 or packing.bit_count() != 1:
    raise ValueError(f"Packing must be <= 8 and a power of 2, got: {packing}")
  if columns % 16:
    raise ValueError(f"Columns must be a multiple of 16, got: {columns}")
  return TMEMLayout(
      fa.Tiling((
          (TMEM_ROWS // 2, columns),
          (fa.WARP_SIZE, columns // 2),
          (packing,),
      )),
      warp_dims=(-4, -5,),
      lane_dims=(-3,),
      vector_dim=-1,
  )

