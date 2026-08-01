
def _mha_reference_fwd(
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
  if save_residuals:
    raise NotImplementedError
  res = _mha_reference(
      q,
      k,
      v,
      ab,
      segment_ids,
      causal=causal,
      mask_value=mask_value,
      sm_scale=sm_scale,
      save_residuals=True,
  )
  assert isinstance(res, tuple)
  out, l, m = res
  return out, (q, k, v, ab, segment_ids, out, l, m)

