
def _get_pull_rule(
    ctx: PullRuleContext, block_transform: BlockIndexTransform, *, tree
):
  if block_transform.block_shape is None:
    return [block_transform] + [no_block_index_transform] * (
        len(ctx.avals_in) - 1
    )
  ref_aval = ctx.avals_in[0]
  assert hasattr(ref_aval, 'shape')
  indexers_avals = tree_util.tree_unflatten(tree, ctx.avals_in[1:])
  if len(indexers_avals) > 1:
    raise NotImplementedError('get not supported yet')
  if not indexers_avals:
    indexer_aval = indexing.NDIndexer.make_trivial_indexer(ref_aval.shape)
  else:
    indexer_aval = indexers_avals[0]
  block_shape_iter = iter(block_transform.block_shape)
  block_shape = []
  if not all(
      bd is None
      or isinstance(bd, (int, pallas_core.Blocked, pallas_core.Squeezed))
      for bd in block_transform.block_shape
  ):
    raise NotImplementedError('get not supported yet')
  for idx_aval, size in zip(indexer_aval.indices, ref_aval.shape, strict=True):
    if not isinstance(idx_aval, indexing.Slice):
      assert hasattr(idx_aval, 'shape') and not idx_aval.shape
      block_shape.append(pallas_core.Squeezed())
      continue
    if not isinstance(idx_aval.start, int):
      raise NotImplementedError('get not supported yet')
    if not isinstance(idx_aval.size, int):
      raise NotImplementedError('get not supported yet')
    if idx_aval.stride != 1:
      raise NotImplementedError('get not supported yet')
    if idx_aval.start != 0:
      raise NotImplementedError('get not supported yet')
    if idx_aval.size != size:
      raise NotImplementedError('get not supported yet')
    bd = next(block_shape_iter)
    block_shape.append(_block_size(bd))
  assert next(block_shape_iter, None) is None

  def new_block_index_transform(*idxs):
    idx = block_transform.block_index_transform(*idxs)
    idx_iter = iter(idx)
    indices = tuple(
        0
        if (bd is None or isinstance(bd, pallas_core.Squeezed))
        else next(idx_iter)
        for bd in range(len(block_shape))
    )
    assert next(idx_iter, None) is None
    return indices

  new_block_transform = block_transform.replace(
      block_shape=block_shape,
      block_index_transform=new_block_index_transform,
  )
  return ([new_block_transform]
          + [no_block_index_transform] * (len(ctx.avals_in) - 1))

