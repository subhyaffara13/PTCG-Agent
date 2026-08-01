
def _get_tiling_factor(src: int, max_tiling: int, packing: int) -> int:
  # This roughly mirrors ``getTilingFactor`` in infer-memref-layout.
  tpu_generation = get_tpu_info().generation
  tiling = (1 + int(tpu_generation < 4)) * packing
  while tiling < min(src, max_tiling):
    tiling *= 2
  return tiling

