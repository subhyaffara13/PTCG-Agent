
def _calculate_irregular_num_tiles(x: int, tx: int) -> tuple[int, int]:
  tiles, rem = divmod(x, tx)
  if rem:
    tiles += 1
  return tiles, rem

