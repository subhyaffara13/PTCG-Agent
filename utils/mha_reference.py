
def mha_reference(
    q,
    k,
    v,
    segment_ids: jnp.ndarray | None,
    sm_scale=1.0,
    causal: bool = False,
):
  q_seq_len = q.shape[1]
  kv_seq_len = k.shape[1]
  logits = jnp.einsum(
      'bqhc,bkhc->bhqk', q, k, preferred_element_type=jnp.float32
  )
  mask = None
  if segment_ids is not None:
    mask = jnp.expand_dims(segment_mask(segment_ids, segment_ids), 1)
    mask = jnp.broadcast_to(mask, logits.shape)
  if causal:
    causal_mask = jnp.tril(jnp.ones((1, 1, q_seq_len, kv_seq_len), dtype=bool))
    causal_mask = jnp.broadcast_to(causal_mask, logits.shape)
    mask = causal_mask if mask is None else jnp.logical_and(mask, causal_mask)
  logits = logits if mask is None else jnp.where(mask, logits, float("-inf"))
  weights = jax.nn.softmax(logits * sm_scale)
  return jnp.einsum(
      'bhqk,bkhc->bqhc', weights, v, preferred_element_type=jnp.float32
  )


def mha_reference(
    q,                # [bs, num_q_heads, head_dim]
    k,                # [bs, k_seq_len, num_k_heads, head_dim]
    v,                # [bs, k_seq_len, num_v_heads, head_dim]
    start_idx=None,   # [bs]
    kv_seq_len=None,  # [bs]
    sm_scale=None,
):
  bs = q.shape[0]
  sm_scale = sm_scale if sm_scale is not None else (1 / math.sqrt(q.shape[-1]))
  assert q.shape[1] == k.shape[2]
  logits = jnp.einsum("bnd,bsnd->bns", q, k).astype(jnp.float32)
  if start_idx is not None or kv_seq_len is not None:
    start_idx = jnp.broadcast_to(0 if start_idx is None else start_idx, (bs,))
    kv_seq_len = jnp.broadcast_to(k.shape[1] if kv_seq_len is None
                                  else kv_seq_len, (bs,))
    mask = ((jnp.arange(k.shape[1])[None, :] >= start_idx[:, None])
            & (jnp.arange(k.shape[1])[None, :] < kv_seq_len[:, None]))
    mask = mask[:, None, :]
    logits = logits + (~mask) * (0.7 * jnp.finfo(logits.dtype).min)
  weights = jax.nn.softmax(logits * sm_scale).astype(q.dtype)
  return jnp.einsum("bns,bsnd->bnd", weights, v)


def mha_reference(
    q,
    k,
    v,
    ab,
    segment_ids: SegmentIds | None = None,
    causal: bool = False,
    mask_value: float = DEFAULT_MASK_VALUE,
    sm_scale=1.0,
):
  return _mha_reference(
      q,
      k,
      v,
      ab,
      segment_ids,
      causal=causal,
      mask_value=mask_value,
      sm_scale=sm_scale,
      save_residuals=False,
  )

