
def _slice_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    start_indices: tuple[int, ...],
    limit_indices: tuple[int, ...],
    strides: tuple[int, ...] | None,
):
  del ctx
  if strides is not None and not all(stride == 1 for stride in strides):
    raise NotImplementedError('strides are not supported yet')
  slice_sizes = tuple(
      int(end - start) for start, end in zip(start_indices, limit_indices)
  )
  # Do some basic checks
  for bs, slice_start, slice_size in zip(
      block_transform.block_shape, start_indices, slice_sizes
  ):
    match bs:
      case None | pallas_core.Squeezed():
        continue
      case pallas_core.BoundedSlice() | pallas_core.Element():
        block_size = _block_size(bs)
        # Require that block_size no bigger than the slice.
        if block_size > slice_size:
          raise ValueError(
              f'Block size {block_size} is larger than the slice size'
              f' {slice_size}'
          )
      case _:
        block_size = _block_size(bs)
        assert slice_start % block_size == 0, (
            start_indices,
            block_transform.block_shape,
        )
        assert slice_size % block_size == 0, (
            slice_sizes,
            block_transform.block_shape,
        )

  def new_block_index_transform(*idxs):
    idx = block_transform.block_index_transform(*idxs)
    assert len(idx) == len(block_transform.block_shape)
    idx = tuple(
        _offset_indexer(bs, i, start, size)
        for bs, i, start, size in zip(
            block_transform.block_shape, idx, start_indices, slice_sizes,
            strict=True
        )
    )
    return idx

  return [block_transform.replace(
      block_index_transform=new_block_index_transform,
  )]

