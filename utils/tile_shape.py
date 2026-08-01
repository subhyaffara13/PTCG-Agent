
def tile_shape(shape, tiling):
  if len(tiling) > len(shape):
    raise ValueError(
        "Expected tiling to be at most rank of shape. Got tiling:"
        f" {tiling} (rank: {len(tiling)}) and shape {shape} (rank:"
        f" {len(shape)})."
    )
  if not tiling:
    return shape
  tiling_rank = len(tiling)
  for s, t in zip(shape[-tiling_rank:], tiling):
    if s % t:
      raise ValueError("Non-divisible tiling:", shape, tiling)
  return (
      *shape[:-tiling_rank],
      *(s // t for s, t in zip(shape[-tiling_rank:], tiling)),
      *tiling,
  )

