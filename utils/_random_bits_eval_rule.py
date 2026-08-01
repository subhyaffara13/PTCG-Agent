
def _random_bits_eval_rule(eval_ctx: KernelEvalContext, key, bit_width, shape):
  del shape
  block_spec = eval_ctx.out_block_specs[0]
  indices = eval_ctx.get_out_block_indices()[0]
  block_shape = block_spec.block_shape
  # This is the important part here: we fold in block indices into the key so
  # each block gets different random numbers.
  for idx in indices:
    key = jax.random.fold_in(key, idx)
  return prng.random_bits(key, bit_width=bit_width, shape=block_shape)

