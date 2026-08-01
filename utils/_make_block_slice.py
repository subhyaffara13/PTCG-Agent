
def _make_block_slice(
    block_index: jax.Array, block_size: BlockDim | int | None, size: int,
    tiling: int | None
) -> Slice | slice | int | jax.Array:
  # Computes a slice given a block index and block size. In the default case,
  # we return slice(block_index * block_size, (block_index + 1) * block_size).
  # However, if the total size of the ref does not divide block size and we are
  # selecting the last block, we need to pick the lowest tiling size multiple
  # that contains the block.
  match block_size:
    case Blocked():
      return _create_blocked_slice(block_index, block_size.block_size, size, tiling)
    case int():
      return _create_blocked_slice(block_index, block_size, size, tiling)
    case Element():
      block_start = block_index
      block_size = block_size.block_size
      return _create_bounded_slice(
          block_start, block_size, block_size, size, tiling
      )
    case BoundedSlice(block_size):
      if not isinstance(block_index, Slice):
        raise ValueError(
            "Must return a ds from the index_map for a BoundedSlice"
            " dimension."
        )
      slice_start = block_index.start
      slice_size = block_index.size
      return _create_bounded_slice(
          slice_start, slice_size, block_size, size, tiling
      )
    case None | Squeezed() | Indirect():
      return block_index
    case _:
      raise ValueError(f"Unsupported block dimension type: {block_size}")

