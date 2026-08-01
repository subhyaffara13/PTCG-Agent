
def splat_is_compatible_with_tiled(
    l1: fa.WGSplatFragLayout, l2: fa.TiledLayout
) -> bool:
  # A splat layout is compatible with a tiled layout up to replication if each
  # dimension in the shape of the splat layout is divisible by the corresponding
  # dimension in the base tile shape.
  s1, s2 = l1.shape, l2.base_tile_shape
  return all(d1 % d2 == 0 for d1, d2 in zip(s1, s2))

