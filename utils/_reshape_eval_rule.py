
def _reshape_eval_rule(
    eval_ctx: KernelEvalContext, x, *, dimensions, new_sizes, sharding
):
  del sharding, dimensions, new_sizes
  out_shape_nones = tuple(
      _block_size(s) for s in eval_ctx.out_block_specs[0].block_shape
  )
  out_shape = tuple(s for s in out_shape_nones if s is not None)
  # Because we have restricted the pull block spec rule, we can just apply a
  # basic reshape here.
  x = x.reshape(out_shape)
  return x

