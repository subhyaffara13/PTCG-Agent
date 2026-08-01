
def _tile_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    reps: tuple[int, ...],
):
  del reps
  block_shape = block_transform.block_shape
  aval_in = ctx.avals_in[0]
  assert isinstance(aval_in, core.ShapedArray)
  assert len(block_shape) == len(aval_in.shape)
  if not all(isinstance(dim, (int, pallas_core.Squeezed))
             for dim in block_shape):
    raise NotImplementedError(
        'tile with non-int block dimensions not supported yet'
    )

  if not all(
      (pallas_core.get_block_size(block_dim) % in_dim == 0) or
      (in_dim % pallas_core.get_block_size(block_dim) == 0)
      for block_dim, in_dim in zip(block_shape, aval_in.shape)
  ):
    raise NotImplementedError(
        'Every block dimension must be either a multiple or factor of input. '
        f'Got block {block_shape} for input {aval_in.shape}'
    )

  new_shape = tuple(
      block_dim if isinstance(block_dim, pallas_core.Squeezed)
      else min(block_dim, in_dim)
      for block_dim, in_dim in zip(block_shape, aval_in.shape)
  )

  def new_block_index_transform(*idxs):
    original_idxs = block_transform.block_index_transform(*idxs)
    return tuple(
        0 if pallas_core.get_block_size(block_dim) >= in_dim
        else orig_idx % (in_dim // pallas_core.get_block_size(block_dim))
        for orig_idx, block_dim, in_dim in zip(
            original_idxs, block_shape, aval_in.shape
        )
    )

  return [block_transform.replace(
      block_shape=new_shape,
      block_index_transform=new_block_index_transform)]

