
def _stack_push_rule(
    ctx: PushRuleContext,
    *block_specs: pallas_core.BlockSpec,
    axis: int,
):
  avals_in = ctx.avals_in
  assert all(hasattr(aval_in, 'shape') for aval_in in avals_in)

  def _new_index_map(*args):
    all_indices = [block_spec.index_map(*args) for block_spec in block_specs]
    if not all(
        (all_indices[0][i] is all_indices[j][i])
        for i in range(len(all_indices[0]))
        for j in range(len(all_indices))
    ):
      raise ValueError(
          'Cannot statically prove that all input blocks to stack are the'
          ' same.'
      )
    base_indices = list(all_indices[0])
    base_indices.insert(axis, 0)
    return tuple(base_indices)

  new_block_shape = list(block_specs[0].block_shape)
  new_block_shape.insert(axis, len(block_specs))

  return pallas_core.BlockSpec(tuple(new_block_shape), _new_index_map)

