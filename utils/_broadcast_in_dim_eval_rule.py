
def _broadcast_in_dim_eval_rule(
    eval_ctx: KernelEvalContext, x, broadcast_dimensions, shape, **params
):
  del params  # Unused.
  in_shape = eval_ctx.avals_in[0].shape
  if in_shape == shape:
    # Dummy broadcast
    return x
  shape = tuple(map(_block_size, eval_ctx.out_block_specs[0].block_shape))
  dims = tuple(
      d - sum(s is None for s in shape[:d])
      for d in broadcast_dimensions
      if shape[d] is not None
  )
  shape = tuple(s for s in shape if s is not None)
  return jax.lax.broadcast_in_dim(x, broadcast_dimensions=dims, shape=shape)

