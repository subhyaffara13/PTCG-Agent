
def _concatenate_push_rule(
    ctx: PushRuleContext,
    *block_specs: pallas_core.BlockSpec,
    dimension: int,
):
  avals_in = ctx.avals_in
  block_shapes = [
      pallas_core._canonicalize_block_shape(block_spec.block_shape)
      for block_spec in block_specs
  ]
  # We only support concatenation if the entirety of the concat dimension is blocked.
  assert all(hasattr(aval_in, 'shape') for aval_in in avals_in)
  if not all(
      block_shape[dimension] == pallas_core.Blocked(avals_in.shape[dimension])
      for block_shape, avals_in in zip(block_shapes, avals_in)
  ):
    raise NotImplementedError(
        f'concatenate not supported yet: {block_shapes=}, {avals_in=}'
    )
  def _new_index_map(*args):
    all_indices = [block_spec.index_map(*args) for block_spec in block_specs]
    # This is a very important check. We cannot actually construct a single BlockSpec
    # for the output of concatenate if the indices are not identical across all the
    # inputs. This is not something we can always enforce statically, but to be conservative
    # we apply a very aggressive check. We can consider relaxing this later.
    if not all(
        (all_indices[0][i] is all_indices[j][i])
        for i in range(len(all_indices[0]))
        for j in range(len(all_indices))
    ):
      raise ValueError(
          'Cannot statically prove that all input blocks to concatenate are the'
          ' same.'
      )
    # If all block indices are the same, we are materializing the full concatenation along
    # the concat dimension, so we use index 0.
    base_indices = list(all_indices[0])
    base_indices[dimension] = 0
    return tuple(base_indices)

  new_block_shape = list(block_specs[0].block_shape)
  # Since the entirety of the concat dimension is materialized in the blocks,
  # the new block size is the sum of the block sizes of the inputs along that
  # dimension.
  new_block_shape[dimension] = sum(
      pallas_core.get_block_size(block_shape[dimension])
      for block_shape in block_shapes
  )
  return pallas_core.BlockSpec(tuple(new_block_shape), _new_index_map)

