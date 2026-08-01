
def _select_n_pull_block_spec_rule(
    ctx: PullRuleContext, block_transform: BlockIndexTransform,
) -> Sequence[BlockIndexTransform]:
  in_aval = ctx.avals_in[0]
  assert isinstance(in_aval, core.ShapedArray)
  if in_aval.shape:
    return [block_transform] * len(ctx.avals_in)
  return [no_block_index_transform, *[block_transform] * (len(ctx.avals_in) - 1)]

