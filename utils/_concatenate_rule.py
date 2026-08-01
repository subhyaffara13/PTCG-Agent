
def _concatenate_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    dimension: int,
):
  block_shape = block_transform.block_shape
  is_element_block = [isinstance(bd, pallas_core.Element) for bd in block_shape]
  if any(is_element_block):
    raise NotImplementedError(
        'Concatenation with Element indexing is not yet supported.'
    )
  num_blocks = []
  block_dim = block_shape[dimension]
  if block_dim is None or isinstance(block_dim, pallas_core.Squeezed):
    block_dim = 1
  if block_dim == sum(aval.shape[dimension] for aval in ctx.avals_in):
    # Handle special case if the block contains all of the concatenated
    # array.
    new_shapes = [
        util.tuple_update(
            block_transform.block_shape, dimension, aval.shape[dimension]
        )
        for aval in ctx.avals_in
    ]
    new_block_transforms = [
        block_transform.replace(block_shape=shape) for shape in new_shapes
    ]
    return new_block_transforms

  # We now handle the case where each of the concatenated array dimensions
  # divides the block size.
  for aval in ctx.avals_in:
    assert isinstance(aval, core.ShapedArray)
    if aval.shape[dimension] % block_dim != 0:
      raise ValueError(
          f'Shape along concat dimension {dimension} must be divisible by the'
          f' block shape {block_shape[dimension]} for all children. Got shape'
          f' {aval.shape}.'
      )
    num_blocks.append(aval.shape[dimension] // block_dim)
  ends = np.cumsum(num_blocks).astype(np.int32)
  starts = np.concatenate(([0], ends[:-1])).astype(np.int32)

  def make_block_transform(child_index: int):
    def new_block_index_transform(*idxs):
      idx = block_transform.block_index_transform(*idxs)
      block_idx = idx[dimension]
      is_valid = (starts[child_index] <= block_idx) & (
          block_idx < ends[child_index]
      )
      padding_index = jnp.where(
          block_idx < starts[child_index], 0, num_blocks[child_index] - 1
      )
      block_idx = jnp.where(
          is_valid, block_idx - starts[child_index], padding_index
      )
      return util.tuple_update(idx, dimension, block_idx)

    return block_transform.replace(
        block_index_transform=new_block_index_transform
    )
  return [make_block_transform(i) for i in range(len(ctx.avals_in))]

