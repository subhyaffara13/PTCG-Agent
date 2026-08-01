
def compute_swizzle(minor_tiling: int, bitwidth: int) -> int:
  """Computes the swizzle for the given minor tiled dimension and bitwidth."""
  tiling_bitwidth = minor_tiling * bitwidth
  if tiling_bitwidth % 8:
    raise ValueError("Minor tiling dimension is not byte aligned. "
                     f"Got {minor_tiling} elements of {bitwidth} bits.")
  tiling_bytewidth = tiling_bitwidth // 8
  # Do not swizzle if the bytewidth of the minor tiling dimension does not
  # exactly match a swizzle width.
  if tiling_bytewidth in [128, 64, 32]:
    return tiling_bytewidth
  return 16  # no swizzle

