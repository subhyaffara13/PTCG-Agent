
def _reduce_sum_eval_rule(
    ctx: KernelEvalContext,
    x,
    *,
    axes: tuple[int, ...],
    out_sharding,
):
  del out_sharding
  aval_in = ctx.avals_in[0]
  assert isinstance(aval_in, core.ShapedArray)
  block_shape = tuple(ctx.in_block_specs[0].block_shape)
  for i in axes:
    if _block_size(block_shape[i]) != aval_in.shape[i]:
      raise NotImplementedError(
          f'reduce_sum on partial blocks not supported: {aval_in=},'
          f' {block_shape=}'
      )
  return jax.lax.reduce_sum(x, axes=axes)

