
def _slice_eval_rule(ctx, x, **params):
  del params
  out_block_shape = ctx.out_block_specs[0].block_shape
  assert len(x.shape) == sum(
      1
      for bs in out_block_shape
      if not (bs is None or isinstance(bs, pallas_core.Squeezed))
  )
  return x

