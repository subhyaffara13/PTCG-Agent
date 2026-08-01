
def tiled_copy_smem_gmem_layout(
    row_tiles: int, col_tiles: int, swizzle: int, bitwidth: int
) -> TiledLayout:
  swizzle_elems = 8 * swizzle // bitwidth
  if row_tiles % 4 == 0:
    warp_row_tiles, warp_col_tiles = 4, 1
  elif row_tiles % 2 == 0:
    if col_tiles % 2:
      raise NotImplementedError("Number of tiles is not a multiple of 4")
    warp_row_tiles, warp_col_tiles = 2, 2
  else:
    if col_tiles % 4:
      raise NotImplementedError("Number of tiles is not a multiple of 4")
    warp_row_tiles, warp_col_tiles = 1, 4
  row_tiles //= warp_row_tiles
  col_tiles //= warp_col_tiles
  bytes_per_thread = min(16, 8 * swizzle // WARP_SIZE)
  lane_row_tiles = lane_col_tiles = 1
  if bytes_per_thread < 16:  # Try to splread multiple tiles over a warp.
    max_scale_up = 16 // bytes_per_thread
    while max_scale_up > 1 and col_tiles % 2 == 0:
      max_scale_up //= 2
      lane_col_tiles *= 2
      col_tiles //= 2
    while max_scale_up > 1 and row_tiles % 2 == 0:
      max_scale_up //= 2
      lane_row_tiles *= 2
      row_tiles //= 2
    bytes_per_thread *= lane_row_tiles * lane_col_tiles
  if 8 * bytes_per_thread < bitwidth:
    raise NotImplementedError("Element types with bitwidth so large aren't supported")
  vector_length = bytes_per_thread * 8 // bitwidth
  assert swizzle_elems % vector_length == 0
  # How many steps of vector transfers are needed to transfer a single tile?
  if vector_length * WARP_SIZE > 8 * swizzle_elems:
    steps_per_tile = 1
  else:
    steps_per_tile = 8 * swizzle_elems // (vector_length * WARP_SIZE)
  tile_rows_per_step = 8 // steps_per_tile
  # There are two cases to consider here: either a single transfer fits within
  # a single tile (lane_row_tiles == lane_col_tiles == 1), which is the case
  # for large swizzles, or it spans multiple tiles. The layout below ensures
  # that consecutive lanes first traverse the columns within a tile, followed
  # by rows within a tile, columns across tiles, and then rows across tiles.
  # This ensures we never end up with bank conflicts, and yields well
  # coalesced GMEM accesses.
  return TiledLayout(
      Tiling(
          (
              (warp_row_tiles * lane_row_tiles * 8, warp_col_tiles * lane_col_tiles * swizzle_elems),
              (lane_row_tiles * 8, lane_col_tiles * swizzle_elems),
              (8, swizzle_elems),
              (tile_rows_per_step, swizzle_elems),
              (vector_length,)
          )
      ),
      warp_dims=(-9, -8),
      lane_dims=(-7, -6, -3, -2),
      vector_dim=-1,
      _check_canonical=False,
  ).canonicalize()

