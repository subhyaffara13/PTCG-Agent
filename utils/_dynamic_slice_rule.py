
def _dynamic_slice_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    slice_sizes: tuple[int, ...],
):

  def new_block_index_transform(*idxs):
    slice_starts = ctx.scalar_prefetch_fn()
    if len(slice_starts) != len(block_transform.block_shape):
      raise ValueError(
          f'Expected {len(block_transform.block_shape)} slice starts, got'
          f' {len(slice_starts)}'
      )
    idx = block_transform.block_index_transform(*idxs)
    assert len(idx) == len(block_transform.block_shape)

    # Once we have the indices, we need to offset them by the dynamic slice
    # indices. The dynamic slice indices index the full array. For example,
    # let's say we have a [l, m, n] array and are provided 3 dynamic slice
    # start indices [i, j, k] with sizes [s_l, s_m, s_n]. To perform the slice,
    # we need to compute the indices of the block that correspond to that slice
    # in the [l, m, n] array. If we have block sizes [b_l, b_m, b_n], we require
    # that i % b_l == 0, j % b_m == 0, k % b_n == 0 and the slice sizes are
    # multiples of the block sizes. The indices of the block that correspond to
    # the slice are then given by (i // b_l, j // b_m, k // b_n).
    # We then add these block indices to block indices produced by the index
    # map
    block_indices = tuple(
        _offset_indexer(s, i, start, size)
        for i, s, start, size in zip(
            idx, block_transform.block_shape, slice_starts, slice_sizes, strict=True
        )
    )
    return block_indices

  new_block_transform = block_transform.replace(
      block_index_transform=new_block_index_transform,
  )
  return [new_block_transform] + [no_block_index_transform] * (len(ctx.avals_in) - 1)

