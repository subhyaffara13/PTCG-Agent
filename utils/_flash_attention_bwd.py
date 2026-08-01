
def _flash_attention_bwd(
    save_residuals: bool,
    causal: bool,
    sm_scale: float,
    block_sizes: BlockSizes,
    debug: bool,
    residuals,
    do,
):
  """VJP rule for FlashAttention."""
  if save_residuals:
    raise NotImplementedError("Higher-order AD not supported")
  (q, k, v, ab, segment_ids, o, l, m) = residuals
  if not block_sizes.has_backward_blocks:
    raise ValueError(
        "Program is being differentiated, but not all backward blocks are"
        " specified"
    )

  di = jnp.sum(
      o.astype(jnp.float32) * do.astype(jnp.float32), axis=-1
  )  # [batch_size, num_heads, q_seq_len]

  dk, dv = _flash_attention_bwd_dkv(
      q,
      k,
      v,
      ab,
      segment_ids,
      l,
      m,
      do,
      di,
      block_q_major=block_sizes.block_q_major_dkv,  # pyrefly: ignore[bad-argument-type]
      block_k_major=block_sizes.block_k_major_dkv,  # pyrefly: ignore[bad-argument-type]
      block_k=block_sizes.block_k_dkv,  # pyrefly: ignore[bad-argument-type]
      block_q=block_sizes.block_q_dkv,  # pyrefly: ignore[bad-argument-type]
      sm_scale=sm_scale,
      causal=causal,
      mask_value=DEFAULT_MASK_VALUE,
      debug=debug,
  )

  dq, ds = _flash_attention_bwd_dq(
      q,
      k,
      v,
      ab,
      segment_ids,
      l,
      m,
      do,
      di,
      block_q_major=block_sizes.block_q_dq,  # pyrefly: ignore[bad-argument-type]
      block_k_major=block_sizes.block_k_major_dq,  # pyrefly: ignore[bad-argument-type]
      block_k=block_sizes.block_k_dq,  # pyrefly: ignore[bad-argument-type]
      sm_scale=sm_scale,
      causal=causal,
      mask_value=DEFAULT_MASK_VALUE,
      debug=debug,
  )
  return dq, dk, dv, ds, None

