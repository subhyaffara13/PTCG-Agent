import random

def blocked_fold_in(
  global_key: ArrayLike,
  total_size: Shape,
  block_size: Shape,
  tile_size: Shape,
  block_index: Sequence[ArrayLike],
  ) -> NdKeyList:
  """Computes a grid of keys for block-invariant sampling.

  Suppose we wished to construct a 16x512 array of random numbers, using
  block sizes of 16x128 and 16x256. We could select an tile size of 8x128
  (which divides both 16x128 and 16x256) and divide the total array in tiles as:
  ---------------------------------
  | 8x128 | 8x128 | 8x128 | 8x128 |
  ---------------------------------
  | 8x128 | 8x128 | 8x128 | 8x128 |
  ---------------------------------

  We generate a key for each tile as:
    tile_key = fold_in(global_key, tile_idx)

  Where the tile_idx is the row-major raveled index of each element:
  -----------------
  | 0 | 1 | 2 | 3 |
  -----------------
  | 4 | 5 | 6 | 7 |
  -----------------

  We then compute and return the keys required to sample the tiles that make
  up the current block (specified via `block_index`).
  With a 16x256 block size, each block requires 4 (2x2) tile keys:
  ---------------
  | 0, 1 | 2, 3 |
  | 4, 5 | 6, 7 |
  ---------------
  Therefore, we return a grid of 2x2 keys for each block (2 blocks total).

  With a 16x128 block size, each block requires 2 (2x1) tile keys:
  -----------------
  | 0 | 1 | 2 | 3 |
  | 4 | 5 | 6 | 7 |
  -----------------
  Therefore, we return a grid of 2x1 keys for each block (4 blocks total).

  Args:
    global_key: The global key shared between all blocks.
    total_size: The shape of the array being generated.
    block_size: The shape of an individual block.
    tile_size: The shape of a `tile`, which is the smallest unit at
      which samples are generated. This should be selected to be a divisor
      of all block sizes one needs to be invariant to.
    block_index: The index denoting which block to generate keys for.

  Returns:
    An N-dimensional nested list of keys required to sample the tiles
    corresponding to the block specified by `block_index`.
  """
  block_size_in_tiles = tuple(
      _shape // _element for _shape, _element in zip(block_size, tile_size)
  )

  # Round up to make sure every tile is numbered.
  total_size_in_tiles = tuple(
      (_shape + _element - 1) // _element
        for _shape, _element in zip(total_size, tile_size)
  )

  def _keygen_loop(axis, prefix):
    if axis == len(block_size_in_tiles):
      subtile_key = random.fold_in(
          global_key, _compute_tile_index(
              block_index, block_size_in_tiles, total_size_in_tiles, prefix))
      return subtile_key
    else:
      keys = []
      for i in range(block_size_in_tiles[axis]):
        keys.append(_keygen_loop(axis+1, prefix+(i,)))
      return keys
  return _keygen_loop(0, ())

