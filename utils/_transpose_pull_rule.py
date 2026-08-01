
def _transpose_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    permutation: tuple[int, ...],
):

  block_shape = block_transform.block_shape
  new_shape = tuple(block_shape[i] for i in permutation)
  aval_in = ctx.avals_in[0]
  assert isinstance(aval_in, core.ShapedArray)
  assert len(block_shape) == len(aval_in.shape)
  if set(permutation[-2:]) != {permutation[-1], permutation[-2]}:
    raise NotImplementedError(
        'Cannot permute last two dimensions with leading dimensions.'
    )

  def new_block_index_transform(*idxs):
    original_idxs = block_transform.block_index_transform(*idxs)
    return tuple(original_idxs[i] for i in permutation)

  return [block_transform.replace(
      block_shape=new_shape,
      block_index_transform=new_block_index_transform)]

