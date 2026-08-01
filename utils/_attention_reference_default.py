
def _attention_reference_default(
    mask: jax.Array,  # [q_seq_len, kv_seq_len]
    q: jax.Array,  # [q_seq_len, head_dim]
    k: jax.Array,  # [kv_seq_len, head_dim]
    v: jax.Array,  # [kv_seq_len, head_dim]
    segment_ids: SegmentIds | None,
    sinks: jax.Array | None,  # [] one scalar per qhead
    mask_value: float,
    save_residuals: bool,
    custom_type: str,
    attn_logits_soft_cap: float | None,
):
  del custom_type
  logits = jnp.einsum("sd,td->st", q.astype(jnp.float32), k.astype(jnp.float32))

  if segment_ids is not None:
    mask = jnp.logical_and(
        mask, segment_ids.q[:, None] == segment_ids.kv[None, :]
    )

  if attn_logits_soft_cap is not None:
    logits = jnp.tanh(logits / attn_logits_soft_cap)
    logits = logits * attn_logits_soft_cap

  logits = jnp.where(mask, logits, mask_value)
  m = logits.max(axis=-1)
  sinks = None if sinks is None else sinks.astype(logits.dtype)
  m = m if sinks is None else jnp.maximum(m, sinks)
  s = jnp.exp(logits - m[..., None])
  l = s.sum(axis=-1) + (0 if sinks is None else jnp.exp(sinks - m))
  s = s / l[..., None]

  o = jnp.einsum("st,td->sd", s, v.astype(jnp.float32))

  logsumexp = m + jnp.log(l)
  if save_residuals:
    return o, (logsumexp,)
  return o

