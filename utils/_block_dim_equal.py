
def _block_dim_equal(
    b1: int | pallas_core.BlockDim | None, b2: int | pallas_core.BlockDim | None
) -> bool:
  block_size1 = pallas_core.get_block_size(b1)
  block_size2 = pallas_core.get_block_size(b2)
  match (b1, b2):
    case (None, _) | (_, None):
      return b1 == b2
    case (
        (pallas_core.Blocked(), int())
        | (int(), pallas_core.Blocked())
        | (pallas_core.Blocked(), pallas_core.Blocked())
        | (int(), int())
    ):
      return block_size1 == block_size2
    case _:
      return type(b1) == type(b2) and (block_size1 == block_size2)

