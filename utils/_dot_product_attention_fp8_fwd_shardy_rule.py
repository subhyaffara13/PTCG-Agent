
def _dot_product_attention_fp8_fwd_shardy_rule(
    scale, use_causal_mask, layout, is_training,
    mesh, value_types, result_types):
  return _fwd_shardy_rule(value_types, result_types, layout, is_training, is_fp8=True)

