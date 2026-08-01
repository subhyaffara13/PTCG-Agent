
def _block_shapes_equal(
    bs1: tuple[int | pallas_core.BlockDim | None] | None,
    bs2: tuple[int | pallas_core.BlockDim | None] | None,
) -> bool:
  if bs1 is None or bs2 is None:
    return bs1 == bs2
  return all(_block_dim_equal(b1, b2) for b1, b2 in zip(bs1, bs2))

