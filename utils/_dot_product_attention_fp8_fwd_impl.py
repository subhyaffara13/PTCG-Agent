
def _dot_product_attention_fp8_fwd_impl(
    query, key, value,
    descale_q, descale_k, descale_v, descale_s, scale_s, scale_o,
    scale, use_causal_mask, layout, is_training):
  outputs = _dot_product_attention_fp8_fwd_p.bind(
      query,
      key,
      value,
      descale_q,
      descale_k,
      descale_v,
      descale_s,
      scale_s,
      scale_o,
      scale=scale,
      use_causal_mask=use_causal_mask,
      layout=layout,
      is_training=is_training,
  )
  return outputs

