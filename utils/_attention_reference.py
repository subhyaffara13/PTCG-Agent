
def _attention_reference(
    mask: jax.Array,
    q: jax.Array,
    k: jax.Array,
    v: jax.Array,
    segment_ids: SegmentIds | None,
    sinks: jax.Array | None,
    mask_value: float,
    save_residuals: Literal[False],
    custom_type: str,
    attn_logits_soft_cap: float | None,
) -> jax.Array:
  ...


def _attention_reference(
    mask: jax.Array,
    q: jax.Array,
    k: jax.Array,
    v: jax.Array,
    segment_ids: SegmentIds | None,
    sinks: jax.Array | None,
    mask_value: float,
    save_residuals: Literal[True],
    custom_type: str,
    attn_logits_soft_cap: float | None,
) -> tuple[jax.Array, tuple[jax.Array]]:
  ...


def _attention_reference(
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
  return _attention_reference_default(
      mask,
      q,
      k,
      v,
      segment_ids,
      sinks,
      mask_value,
      save_residuals,
      custom_type,
      attn_logits_soft_cap,
  )

