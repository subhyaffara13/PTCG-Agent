
def _flash_attention_fwd(
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
  if save_residuals:
    raise NotImplementedError("Higher-order AD not supported")
  o, l, m = _flash_attention(
      q, k, v, ab, segment_ids, True, causal, sm_scale, block_sizes, debug
  )
  return o, (q, k, v, ab, segment_ids, o, l, m)

