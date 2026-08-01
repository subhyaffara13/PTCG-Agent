
def _dot_product_attention_fp8_fwd_rule(
    query, key, value,
    fp8_params,
    scale, use_causal_mask, layout, cudnn_version):
  check_is_flash_attention_fp8(
      query, key, value, layout, cudnn_version, is_training=True)

  outputs = _dot_product_attention_fp8_fwd_p_wrapper.bind(
      query, key, value, *params_from_keys(fp8_params, fp8_params_keys_fwd),
      scale=scale, use_causal_mask=use_causal_mask, layout=layout, is_training=True)
  res = (query, key, value, outputs[3], outputs[0], params_from_keys(fp8_params, fp8_params_keys_bwd))
  return (outputs[0], outputs[1], outputs[2]), res

