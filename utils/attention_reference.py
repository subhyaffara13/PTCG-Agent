import math


def attention_reference(q, k, v, causal=False, save_residuals=False):
  batch_size, q_seq_len, num_q_heads, head_dim = q.shape
  kv_seq_len, num_kv_heads = k.shape[1], k.shape[2]
  q, k, v = map(lambda x: x.astype(jnp.float32), (q, k, v))
  q_reshaped = q.reshape(
      batch_size, q_seq_len, num_kv_heads, num_q_heads // num_kv_heads, head_dim
  )
  logits = jnp.einsum("bqHhc,bkHc->bqHhk", q_reshaped, k)

  if causal:
    mask = jnp.arange(q_seq_len)[:, None] >= jnp.arange(kv_seq_len)[None, :]
    mask = jnp.broadcast_to(mask[:, None, None, :], logits.shape)
    logits = jnp.where(mask, logits, -jnp.inf)

  m = logits.max(axis=-1, keepdims=True)
  unnormalized = jnp.exp(logits - m)
  l = unnormalized.sum(axis=-1, keepdims=True)
  weights = unnormalized / l
  out = jnp.einsum("bqHhk,bkHc->bqHhc", weights, v).reshape(*q.shape)

  if save_residuals:
    log2e = math.log2(math.e)
    l = l.reshape(*q.shape[:-1])
    m = m.reshape(*q.shape[:-1])
    lse = m * log2e + jnp.log2(l)
    return out, (lse.swapaxes(-1, -2),)
  else:
    return out


def attention_reference(
    mask: jax.Array,  # [q_seq_len, kv_seq_len]
    q: jax.Array,  # [q_seq_len, head_dim]
    k: jax.Array,  # [kv_seq_len, head_dim]
    v: jax.Array,  # [kv_seq_len, head_dim]
    segment_ids: SegmentIds | None,
    sinks: jax.Array | None = None,
    *,
    mask_value: float = DEFAULT_MASK_VALUE,
    save_residuals: bool = False,
    custom_type: str = "flash",
    attn_logits_soft_cap: float | None = None,
) -> SplashCustomReturnType:
  return _attention_reference(
      mask,
      q,
      k,
      v,
      segment_ids,
      sinks,
      mask_value=mask_value,
      save_residuals=save_residuals,
      custom_type=custom_type,
      attn_logits_soft_cap=attn_logits_soft_cap,
  )

