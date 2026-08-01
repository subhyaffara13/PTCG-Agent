
def attention_reference_custom(
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
):
  return _attention_reference_custom(
      mask,
      q,
      k,
      v,
      segment_ids,
      sinks,
      mask_value,
      save_residuals,
      custom_type=custom_type,
      attn_logits_soft_cap=attn_logits_soft_cap,
  )

