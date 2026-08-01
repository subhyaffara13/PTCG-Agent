
def _offset_indexer(
    bs: pallas_core.BlockDim | int | None,
    indexer,
    slice_start,
    slice_size,
):
  # Short-circuit if the slice start is just at zero.
  if isinstance(slice_start, int) and slice_start == 0:
    return indexer
  match bs:
    case None | pallas_core.Squeezed():
      return indexer + slice_start
    case pallas_core.Element(block_size):
      _maybe_static_check(
          slice_start % block_size == 0,
          f'slice_start is not a multiple of block_size {block_size}',
      )
      _maybe_static_check(
          slice_size % block_size == 0,
          f'slice_size is not a multiple of block_size {block_size}',
      )
      return indexer + slice_start
    case int() | pallas_core.Blocked():
      block_size = _block_size(bs)
      _maybe_static_check(
          slice_start % block_size == 0,
          f'slice_start is not a multiple of block_size {block_size}',
      )
      _maybe_static_check(
          slice_size % block_size == 0,
          f'slice_size is not a multiple of block_size {block_size}',
      )
      # indexer is a block index so we need to offset it by the block offset.
      return indexer + slice_start // block_size
    case pallas_core.BoundedSlice(block_size):
      assert isinstance(indexer, indexing.Slice)
      _maybe_static_check(
          indexer.start % block_size == 0,
          f'slice_start is not a multiple of block_size {block_size}',
      )
      _maybe_static_check(
          indexer.size % block_size == 0,
          f'slice_size is not a multiple of block_size {block_size}',
      )
      return indexing.ds(indexer.start + slice_start, indexer.size)
    case _:
      raise ValueError(f'Unsupported block size {bs}')

