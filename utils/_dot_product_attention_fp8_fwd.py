
def _dot_product_attention_fp8_fwd(
    query, key, value,
    fp8_params_fwd,
    scale, use_causal_mask, layout, cudnn_version):
  check_is_flash_attention_fp8(
      query, key, value, layout, cudnn_version, is_training=False)
  descale_q, descale_k, descale_v, descale_s, scale_s, scale_o = fp8_params_fwd
  outputs = _dot_product_attention_fp8_fwd_p_wrapper.bind(
      query, key, value,
      descale_q, descale_k, descale_v, descale_s,
      scale_s, scale_o,
      scale=scale, use_causal_mask=use_causal_mask, layout=layout, is_training=False)
  return outputs

