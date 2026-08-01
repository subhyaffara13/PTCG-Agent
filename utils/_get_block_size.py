
def _get_block_size(bd: pl.BlockDim | int | None) -> int:
  match bd:
    case int():
      return bd
    case pl.Blocked() | pl.Element():
      return bd.block_size
    case _:
      raise NotImplementedError(f"Unsupported block size type: {type(bd)}")

