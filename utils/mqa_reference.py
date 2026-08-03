import math


def mqa_reference(
    q,                # [bs, num_q_heads, head_dim]
    k,                # [bs, k_seq_len, head_dim]
    v,                # [bs, k_seq_len, head_dim]
    start_idx=None,   # [bs]
    kv_seq_len=None,  # [bs]
    sm_scale=None,
    return_residuals=False,
    normalize_output=True,
):
  original_dtype = q.dtype
  q = q.astype(jnp.float32)
  k = k.astype(jnp.float32)
  bs = q.shape[0]
  sm_scale = sm_scale if sm_scale is not None else (1 / math.sqrt(q.shape[-1]))
  logits = jnp.einsum("bnd,bsd->bns", q, k).astype(jnp.float32)
  if sm_scale is not None and sm_scale != 1.0:
    logits = logits * sm_scale
  if start_idx is not None or kv_seq_len is not None:
    start_idx = jnp.broadcast_to(0 if start_idx is None else start_idx, (bs,))
    kv_seq_len = jnp.broadcast_to(k.shape[1] if kv_seq_len is None
                                  else kv_seq_len, (bs,))
    mask = ((jnp.arange(k.shape[1])[None, :] >= start_idx[:, None])
            & (jnp.arange(k.shape[1])[None, :] < kv_seq_len[:, None]))
    mask = mask[:, None, :]
    logits = logits + (~mask) * (0.7 * jnp.finfo(logits.dtype).min)

  m = logits.max(axis=-1)
  s = jnp.exp(logits - m[..., None])
  l = s.sum(axis=-1)
  if normalize_output:
    s = s / l[..., None]
  o = jnp.einsum("bns,bsd->bnd", s, v).astype(original_dtype)

  if return_residuals:
    return o, (l, m)
  else:
    return o

