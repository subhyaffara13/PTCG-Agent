
def tmem_default_layout(packing: int = 1) -> TMEMLayout:
  """A TMEM layout used for 1CTA MMA with M=128 and 2CTA MMA with M=256."""
  if packing.bit_count() != 1:
    raise ValueError(f"Packing must be a power of 2, got: {packing}")
  return TMEMLayout(
      fa.Tiling(((TMEM_ROWS, packing), (fa.WARP_SIZE, packing))),
      warp_dims=(-4,),
      lane_dims=(-2,),
      vector_dim=-1,
  )

