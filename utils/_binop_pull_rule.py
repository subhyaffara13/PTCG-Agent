
def _binop_pull_rule(prim, ctx: PullRuleContext, block_transform, **params):
  del prim
  del params  # unused
  l_block_transform = block_transform
  r_block_transform = block_transform
  left_aval, right_aval = ctx.avals_in
  assert isinstance(left_aval, core.ShapedArray)
  assert isinstance(right_aval, core.ShapedArray)

  if not right_aval.shape:
    return [block_transform, no_block_index_transform]
  if not left_aval.shape:
    return [no_block_index_transform, block_transform]
  for i, (l, r) in enumerate(
      zip(left_aval.shape, right_aval.shape, strict=True)
  ):
    if l == 1 and r != 1:
      l_block_transform = _pull_bcast_block_spec(l_block_transform, i)
    if r == 1 and l != 1:
      r_block_transform = _pull_bcast_block_spec(r_block_transform, i)

  return [l_block_transform, r_block_transform]

