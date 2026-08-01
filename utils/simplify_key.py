
def simplify_key(key):
  """Simplify the key to reduce the number of combinations."""
  (
      q_dtype,
      kv_dtype,
      num_q_heads_per_blk,
      num_kv_heads_per_blk,
      head_dim,
      page_size,
      max_num_batched_tokens,
      pages_per_seq,
  ) = key
  return (
      jnp.dtype(q_dtype).name,
      jnp.dtype(kv_dtype).name,
      next_power_of_2(num_q_heads_per_blk),
      next_power_of_2(num_kv_heads_per_blk),
      (head_dim + 127) // 128 * 128,
      next_power_of_2(page_size),
      next_power_of_2(max_num_batched_tokens),
      next_power_of_2(page_size * pages_per_seq),
  )

