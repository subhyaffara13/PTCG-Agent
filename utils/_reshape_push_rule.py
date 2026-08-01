
def _reshape_push_rule(
    ctx: PullRuleContext,
    block_spec: pallas_core.BlockSpec,
    *,
    dimensions: tuple[int, ...] | None,
    new_sizes: tuple[int, ...],
    sharding: jax.sharding.Sharding,
):
  del sharding, new_sizes
  if dimensions is not None:
    raise NotImplementedError('reshape with None dimensions not supported yet')
  aval_in = ctx.avals_in[0]
  assert isinstance(aval_in, core.ShapedArray)
  aval_out = ctx.avals_out[0]
  assert isinstance(aval_out, core.ShapedArray)
  if _pattern_match_lanes_to_sublanes_reshape(aval_in, aval_out):
    block_shape = tuple(block_spec.block_shape)
    if not isinstance(block_shape[-1], (int, pallas_core.Blocked)):
      raise NotImplementedError(
          f'reshape must use Blocked block size on lanes: {block_shape}'
      )
    last_dim = aval_out.shape[-1]
    last_block_dim = _block_size(block_shape[-1])
    if last_block_dim % 128 != 0:
      raise NotImplementedError(
          'reshape with non-128 aligned block size on lanes not supported yet'
      )
    if last_block_dim % last_dim != 0:
      raise NotImplementedError(
          'reshape with non-divisible block size on lanes not supported yet'
      )
    num_last_dim_blocks = last_block_dim // last_dim
    new_block_shape = block_shape[:1] + (num_last_dim_blocks, last_dim)

    def new_index_map(*args):
      *idx, last = block_spec.index_map(*args)
      return *idx, last, 0

    return pallas_core.BlockSpec(new_block_shape, new_index_map)
  raise NotImplementedError(f'reshape not supported yet: {aval_in}, {aval_out}')

