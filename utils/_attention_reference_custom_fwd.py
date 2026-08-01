
def _attention_reference_custom_fwd(
    mask: jax.Array,  # [q_seq_len, kv_seq_len]
    q: jax.Array,  # [q_seq_len, head_dim]
    k: jax.Array,  # [kv_seq_len, head_dim]
    v: jax.Array,  # [kv_seq_len, head_dim]
    segment_ids: SegmentIds | None,
    sinks: jax.Array | None,
    mask_value: float,
    save_residuals: bool,
    custom_type: str,
    attn_logits_soft_cap: float | None,
):
  if save_residuals:
    raise NotImplementedError("Higher-order AD not supported.")

  o, (logsumexp,) = _attention_reference(
      mask,
      q,
      k,
      v,
      segment_ids,
      sinks,
      mask_value=mask_value,
      save_residuals=True,
      custom_type=custom_type,
      attn_logits_soft_cap=attn_logits_soft_cap,
  )
  return o, (mask, q, k, v, segment_ids, sinks, o, logsumexp)

