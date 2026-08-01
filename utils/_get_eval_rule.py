
def _get_eval_rule(ctx: KernelEvalContext, ref, *idx, tree):
  indexers = tree_util.tree_unflatten(tree, idx)
  ref_aval = ctx.avals_in[0]
  indexers_avals = tree_util.tree_unflatten(tree, ctx.avals_in[1:])
  ref_block_spec = ctx.in_block_specs[0]
  assert hasattr(ref_aval, 'shape')
  if len(indexers) > 1:
    raise NotImplementedError('get not supported yet')
  if not indexers:
    indexer = indexing.NDIndexer.make_trivial_indexer(ref_aval.shape)
    indexer_aval = indexer
  else:
    indexer = indexers[0]
    indexer_aval = indexers_avals[0]
  block_indexer = []

  def _slice(i, b):
    match b:
      case int():
        return indexing.ds(i * b, b)
      case pallas_core.Blocked(bs):
        return indexing.ds(i * bs, bs)
      case pallas_core.Squeezed() | None:
        return i
      case _:
        raise NotImplementedError('get not supported yet')

  if (
      ref_block_spec is pallas_core.no_block_spec
      or ref_block_spec.block_shape is None
  ):
    # Short-circuit if the ref is not blocked.
    return state_primitives.get_p.bind(ref, *idx, tree=tree)
  block_idx_iter = iter(ctx.get_out_block_indices()[0])
  for idx_aval, size, idx, bd in zip(
      indexer_aval.indices,
      ref_aval.shape,
      indexer.indices,
      ref_block_spec.block_shape,
      strict=True,
  ):
    if not isinstance(idx_aval, indexing.Slice):
      assert hasattr(idx_aval, 'shape') and not idx_aval.shape, idx_aval
      assert bd is None or isinstance(bd, pallas_core.Squeezed)
      block_indexer.append(idx)
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
    bidx = next(block_idx_iter)
    block_indexer.append(_slice(bidx, bd))
  assert next(block_idx_iter, None) is None
  return ref.get(idx=tuple(block_indexer))

