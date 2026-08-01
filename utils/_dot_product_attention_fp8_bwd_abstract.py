
def _dot_product_attention_fp8_bwd_abstract(
    query, key, value, fwd_output, grad_output, activation,
    descale_q, descale_k, descale_v, descale_o, descale_dO, descale_s,
    descale_dP, scale_s, scale_dQ, scale_dK, scale_dV, scale_dP,
    scale, use_causal_mask, layout):
  amax_shape = (1,1,1,1)
  return (
    _attention_out_aval(query),
    _attention_out_aval(key),
    _attention_out_aval(value),
    core.ShapedArray(amax_shape, np.float32),
    core.ShapedArray(amax_shape, np.float32),
    core.ShapedArray(amax_shape, np.float32),
    core.ShapedArray(amax_shape, np.float32),
  )

