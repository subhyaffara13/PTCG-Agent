
def _reduce_sum_push_rule(
    ctx: PushRuleContext,
    block_spec: pallas_core.BlockSpec,
    *,
    axes: tuple[int, ...],
    out_sharding,
):
  del out_sharding
  aval_in = ctx.avals_in[0]
  assert isinstance(aval_in, core.ShapedArray)
  if not all(
      aval_in.shape[i] == pallas_core.get_block_size(block_spec.block_shape[i])
      for i in axes
  ):
    raise NotImplementedError(
        f'reduce_sum over partial blocks not supported yet: {aval_in.shape=},'
        f' {block_spec.block_shape=}, {axes=}'
    )
  new_block_shape = tuple(
      bd for i, bd in enumerate(block_spec.block_shape) if i not in axes
  )

  def new_index_map(*args):
    idx = block_spec.index_map(*args)
    return tuple(idx[i] for i in range(len(idx)) if i not in axes)

  return block_spec.replace(
      block_shape=tuple(new_block_shape), index_map=new_index_map
  )

