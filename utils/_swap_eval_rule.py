
def _swap_eval_rule(ctx: KernelEvalContext, ref, val, *idx, tree):
  indexers = tree_util.tree_unflatten(tree, idx)
  ref_aval, _ = ctx.avals_in[:2]
  indexers_avals = tree_util.tree_unflatten(tree, ctx.avals_in[2:])
  assert hasattr(ref_aval, 'shape')
  if len(indexers) > 1:
    raise NotImplementedError('swap not supported yet')
  if not indexers_avals:
    indexer_aval = indexing.NDIndexer.make_trivial_indexer(ref_aval.shape)
  else:
    indexer_aval = indexers_avals[0]
  for idx_aval, size in zip(indexer_aval.indices, ref_aval.shape, strict=True):
    if not isinstance(idx_aval, indexing.Slice):
      raise NotImplementedError('swap not supported yet')
    if not isinstance(idx_aval.start, int):
      raise NotImplementedError('swap not supported yet')
    if not isinstance(idx_aval.size, int):
      raise NotImplementedError('swap not supported yet')
    if idx_aval.stride != 1:
      raise NotImplementedError('swap not supported yet')
    if idx_aval.start != 0:
      raise NotImplementedError('swap not supported yet')
    if idx_aval.size != size:
      raise NotImplementedError('swap not supported yet')
  # We have a pure slice so now we can just re-index the ref according to the
  # block indices.
  block_spec = ctx.out_block_specs[0]
  block_idx = ctx.get_out_block_indices()[0]

  def _slice(i, b):
    if not isinstance(b, int):
      raise NotImplementedError('swap not supported yet')
    return i if b is None else indexing.ds(i * b, b)

  indexer = tuple(
      _slice(i, b)
      for i, b in zip(block_idx, block_spec.block_shape, strict=True)
  )
  return ref.swap(val, idx=indexer)

