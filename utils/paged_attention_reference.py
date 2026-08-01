
def paged_attention_reference(
    q: jax.Array,
    k: jax.Array,
    v: jax.Array,
    lengths: jax.Array,
    *,
    mask_value: float = DEFAULT_MASK_VALUE,
    attn_logits_soft_cap: float | None = None,
) -> jax.Array:
  """Grouped query attention reference implementation.

  Args:
    q: A [batch_size, num_heads, head_dim] jax.Array.
    k: A [batch_size, kv_seq_len, num_kv_heads, head_dim] jax.Array.
    v: A [batch_size, kv_seq_len, num_kv_heads, head_dim] jax.Array.
    lengths: A i32[batch_size] jax.Array the length of each example.
    mask_value: The value used for padding in attention. By default it is a very
      negative floating point number.
    attn_logits_soft_cap: The value used for soft capping the attention logits.

  Returns:
    The output of attention([batch_size, num_heads, head_dim]).
  """
  batch_size, num_heads, head_dim = q.shape
  _, kv_seq_len, num_kv_heads, _ = k.shape

  q_heads_per_kv_head = num_heads // num_kv_heads
  q_reshaped = q.reshape(
      batch_size, num_kv_heads, q_heads_per_kv_head, head_dim
  )
  k_transposed = jnp.swapaxes(
      k, 1, 2
  )  # [batch_size, num_kv_heads, kv_seq_len, head_dim]
  v_transposed = jnp.swapaxes(
      v, 1, 2
  )  # [batch_size, num_kv_heads, kv_seq_len, head_dim]

  uncapped_logits = jnp.einsum(
      "bkgd,bksd->bkgs", q_reshaped, k_transposed,
      preferred_element_type=jnp.float32
  ).astype(jnp.float32)

  if attn_logits_soft_cap is not None:
    logits = jnp.tanh(uncapped_logits / attn_logits_soft_cap)
    logits = logits * attn_logits_soft_cap
  else:
    logits = uncapped_logits

  if lengths is not None:
    mask = jnp.arange(kv_seq_len)[None, :] < lengths[:, None]
    mask = jnp.broadcast_to(mask[:, None, None, :], logits.shape)
    logits = jnp.where(mask, logits, mask_value)

  weights = jax.nn.softmax(logits, axis=-1)
  o = jnp.einsum(
      "bkgs,bksd->bkgd", weights, v_transposed.astype(jnp.float32),
      preferred_element_type=jnp.float32
  ).astype(q.dtype)
  o = o.reshape(q.shape)

  return o

