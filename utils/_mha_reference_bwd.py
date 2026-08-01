
def _mha_reference_bwd(
    causal: bool,
    mask_value: float,
    sm_scale: float,
    save_residuals: bool,
    residuals,
    do,
):
  del save_residuals
  q, k, v, ab, segment_ids, o, l, m = residuals
  dq, dk, dv, dab = mha_reference_bwd(
      q,
      k,
      v,
      ab,
      segment_ids,
      o,
      l,
      m,
      do,
      causal=causal,
      mask_value=mask_value,
      sm_scale=sm_scale,
  )
  return dq, dk, dv, dab, None

