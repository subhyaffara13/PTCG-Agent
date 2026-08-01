
def _transpose_push_rule(
    ctx: PushRuleContext,
    block_spec: pallas_core.BlockSpec,
    *,
    permutation: tuple[int, ...],
) -> pallas_core.BlockSpec:
  del ctx
  block_shape = block_spec.block_shape
  new_shape = tuple(block_shape[i] for i in permutation)
  if set(permutation[-2:]) != {permutation[-1], permutation[-2]}:
    raise NotImplementedError(
        'Cannot permute last two dimensions with leading dimensions.'
    )

  def new_index_map(*args):
    original_idxs = block_spec.index_map(*args)
    return tuple(original_idxs[i] for i in permutation)

  return pallas_core.BlockSpec(new_shape, new_index_map)

