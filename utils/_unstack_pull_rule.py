
def _unstack_pull_rule(
    ctx: PullRuleContext,
    out_block_transforms: tuple[BlockIndexTransform, ...],
    *,
    axis: int,
):
  valid_transforms = [
      bt for bt in out_block_transforms if bt is not no_block_index_transform
  ]
  if not valid_transforms:
    return [no_block_index_transform]

  block_transform = valid_transforms[0]
  n = len(out_block_transforms)

  new_block_shape = list(block_transform.block_shape)
  new_block_shape.insert(axis, pallas_core.Blocked(n))

  def new_block_index_transform(*idxs):
    idx = list(block_transform.block_index_transform(*idxs))
    idx.insert(axis, 0)
    return tuple(idx)

  new_block_transform = block_transform.replace(
      block_shape=tuple(new_block_shape),
      block_index_transform=new_block_index_transform
  )
  return [new_block_transform]

