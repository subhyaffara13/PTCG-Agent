
def _dot_product_attention_fp8(query: Array,
                               key: Array,
                               value: Array,
                               fp8_params: dict[str, Array],
                               scale: float,
                               use_causal_mask: bool,
                               layout: int,
                               cudnn_version: int):
  output, amax_s, amax_o = _dot_product_attention_fp8_fwd(
      query, key, value, params_from_keys(fp8_params, fp8_params_keys_fwd),
      scale, use_causal_mask, layout, cudnn_version
  )
  return output, amax_s, amax_o

