
def _infer_tmem_layout(shape: tuple[int, ...], collective: bool, packing: int) -> TMEMLayout:
  if len(shape) != 2:
    raise ValueError(f"TMEM can only represent 2D shapes, got {shape}")
  if packing > 8 or packing.bit_count() != 1:
    raise ValueError(f"Packing must be <= 8 and a power of 2, got: {packing}")
  if shape[1] % packing:
    raise ValueError(f"Minor dimension of shape must be divisible by packing, got: {shape}")
  if shape[0] == TMEM_ROWS:
    return tmem_default_layout(packing)
  elif shape[0] == TMEM_ROWS // 2:
    if collective:
      return tmem_m64_collective_layout(shape[1], packing)
    else:
      return tmem_half_lane_layout(shape[1], packing)
  else:
    raise ValueError(
        f"Unsupported shape: {shape}. TMEM references must have either"
        f" {TMEM_ROWS} or {TMEM_ROWS // 2} rows, but got {shape[0]}."
    )

