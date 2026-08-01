
def _flash_attention(
    q,
    k,
    v,
    ab,
    segment_ids,
    save_residuals,
    causal,
    sm_scale,
    block_sizes,
    debug,
):
  return _flash_attention_impl(
      q,
      k,
      v,
      ab,
      segment_ids,
      save_residuals,
      causal,
      sm_scale,
      block_sizes.block_b,
      block_sizes.block_q,
      block_sizes.block_k_major,
      block_sizes.block_k,
      debug,
  )

