
def _stack_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    axis: int,
):
  block_shape = block_transform.block_shape
  is_element_block = [isinstance(bd, pallas_core.Element) for bd in block_shape]
  if any(is_element_block):
    raise NotImplementedError(
        'Stack with Element indexing is not yet supported.'
    )
  block_dim = block_shape[axis]
  if block_dim is None or isinstance(block_dim, pallas_core.Squeezed):
    block_dim = 1

  n = len(ctx.avals_in)
  if block_dim != n:
    raise NotImplementedError(
        "Stacking only supported when the block size along the stack axis "
        f"equals the number of inputs. Got block_dim={block_dim}, expected {n}."
    )

  new_block_shape = list(block_transform.block_shape)
  new_block_shape.pop(axis)

  def make_block_transform(child_index: int):
    def new_block_index_transform(*idxs):
      idx = list(block_transform.block_index_transform(*idxs))
      idx.pop(axis)
      return tuple(idx)

    return block_transform.replace(
        block_shape=tuple(new_block_shape),
        block_index_transform=new_block_index_transform
    )

  return [make_block_transform(i) for i in range(n)]

