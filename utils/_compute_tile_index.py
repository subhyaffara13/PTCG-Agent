
def _compute_tile_index(block_index: Sequence[ArrayLike],
                        block_size_in_tiles: Shape,
                        total_size_in_tiles: Shape,
                        tile_index_in_block: Sequence[ArrayLike]) -> ArrayLike:
  ndims = len(block_index)
  dim_size: ArrayLike = 1
  total_idx: ArrayLike = 0
  for i in range(ndims-1, -1, -1):
    dim_idx = tile_index_in_block[i] + block_index[i] * block_size_in_tiles[i]
    total_idx += dim_idx * dim_size
    dim_size *= total_size_in_tiles[i]
  return total_idx

