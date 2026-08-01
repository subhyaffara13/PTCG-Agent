
def _mha_reference(
    q,
    k,
    v,
    ab,
    segment_ids: SegmentIds | None,
    causal: bool,
    mask_value: float,
    sm_scale: float,
    save_residuals: bool,
):
  return mha_reference_no_custom_vjp(
      q,
      k,
      v,
      ab,
      segment_ids,
      causal=causal,
      mask_value=mask_value,
      sm_scale=sm_scale,
      save_residuals=save_residuals,
  )

