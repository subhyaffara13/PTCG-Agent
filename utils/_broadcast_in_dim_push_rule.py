
def _broadcast_in_dim_push_rule(
    ctx: PushRuleContext,
    block_spec: pallas_core.BlockSpec,
    *,
    shape: tuple[int, ...],
    broadcast_dimensions: tuple[int, ...],
    sharding: jax.sharding.Sharding,
):
  del sharding
  in_aval = ctx.avals_in[0]
  assert isinstance(in_aval, core.ShapedArray)
  in_shape = in_aval.shape

  dim_map = {
      out_dim: in_dim
      for in_dim, out_dim in enumerate(broadcast_dimensions)
  }

  new_block_shape = []
  for i, s in enumerate(shape):
    if i in dim_map:
      in_dim = dim_map[i]
      if in_shape[in_dim] != s:
        assert pallas_core.get_block_size(block_spec.block_shape[in_dim]) == 1
        new_block_shape.append(s)
      else:
        new_block_shape.append(block_spec.block_shape[in_dim])
    else:
      new_block_shape.append(s)

  def new_index_map(*args):
    idx = block_spec.index_map(*args)
    return tuple(
        idx[dim_map[i]] if i in dim_map else 0 for i in range(len(shape))
    )

  return pallas_core.BlockSpec(tuple(new_block_shape), new_index_map)

