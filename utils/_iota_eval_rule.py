
def _iota_eval_rule(
    eval_ctx: KernelEvalContext, *, dimension, shape, dtype, sharding
):
  del sharding
  block_spec = eval_ctx.out_block_specs[0]
  block_idx = eval_ctx.get_out_block_indices()[0]
  assert len(block_idx) == len(shape)
  iota_shape = tuple(
      _block_size(s) for s in block_spec.block_shape if s is not None
  )
  dim_ = dimension - sum(
      _block_size(s) is None for s in block_spec.block_shape[:dimension]
  )
  local_iota = jax.lax.broadcasted_iota(dtype, iota_shape, dim_)
  return local_iota + block_idx[dimension] * _block_size(
      block_spec.block_shape[dimension]
  )

