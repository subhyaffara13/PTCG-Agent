
def _dot_product_attention_fp8_bwd_impl(
    query, key, value, fwd_output, grad_output, activation,
    descale_q, descale_k, descale_v, descale_o, descale_dO, descale_s,
    descale_dP, scale_s, scale_dQ, scale_dK, scale_dV, scale_dP,
    scale, use_causal_mask, layout):
  grads = _dot_product_attention_fp8_bwd_p.bind(
      query, key, value, fwd_output, grad_output, activation,
      descale_q, descale_k, descale_v, descale_o, descale_dO, descale_s,
      descale_dP, scale_s, scale_dQ, scale_dK, scale_dV, scale_dP,
      scale=scale, use_causal_mask=use_causal_mask, layout=layout)
  return grads

