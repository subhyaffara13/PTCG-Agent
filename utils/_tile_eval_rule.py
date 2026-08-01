
def _tile_eval_rule(
    eval_ctx: KernelEvalContext, x, reps: tuple[int, ...]
):
  block_spec = eval_ctx.out_block_specs[0]
  block_shape = tuple(d for d in block_spec.block_shape
                      if not isinstance(d, pallas_core.Squeezed))
  if not all(isinstance(dim, int) for dim in block_shape):
    raise NotImplementedError(
        'tile with non-int block dimensions not supported yet'
    )
  if not all(
      out_dim % in_dim == 0 for out_dim, in_dim in zip(block_shape, x.shape)
  ):
    raise NotImplementedError(
        'Block size must be a multiple of the input size. '
        f'Got block {block_shape=} but input {x.shape}.'
    )
  reps_in_block = [
      out_dim // in_dim if out_dim >= in_dim else 1
      for out_dim, in_dim in zip(block_shape, x.shape)
  ]
  return lax.tile(x, reps_in_block)

