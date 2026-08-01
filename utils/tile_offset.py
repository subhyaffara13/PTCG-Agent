
def tile_offset(
    offsets: tuple[int, ...], tiling: tuple[int, ...]
) -> tuple[int, ...]:
  """Tiles the trailing offsets in `offsets` according to `tiling`.

  Raises if the offsets are not aligned with the start of a tile.
  """
  if len(offsets) < len(tiling):
    raise ValueError(f"Offsets {offsets} have lower rank than tiling {tiling}")
  untiled_offsets, tiled_offsets = (
      offsets[: -len(tiling)],
      offsets[-len(tiling) :],
  )
  for i, t in zip(tiled_offsets, tiling, strict=True):
    if i % t != 0:
      raise ValueError(f"Offset {i} is not divisible by tile size {t}")
  return (
      *untiled_offsets,
      *[i // t for i, t in zip(tiled_offsets, tiling, strict=True)],
      *[0] * len(tiling),
  )

