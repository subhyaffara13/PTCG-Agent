
def _unstack_push_rule(
    ctx: PushRuleContext,
    block_spec: pallas_core.BlockSpec,
    *,
    axis: int,
):
  aval_in = ctx.avals_in[0]
  assert isinstance(aval_in, core.ShapedArray)
  block_shape = pallas_core._canonicalize_block_shape(block_spec.block_shape)

  n = aval_in.shape[axis]
  if block_shape[axis] != pallas_core.Blocked(n):
    raise NotImplementedError(
        f'unstack not supported yet: {block_shape=}, {aval_in=}, {axis=}'
    )

  new_block_shape = list(block_spec.block_shape)
  new_block_shape.pop(axis)

  def _new_index_map(*args):
    idx = list(block_spec.index_map(*args))
    idx.pop(axis)
    return tuple(idx)

  out_block_spec = pallas_core.BlockSpec(tuple(new_block_shape), _new_index_map)
  return [out_block_spec] * n

