
def _dot_product_attention_fp8_bwd_shardy_rule(
    scale, use_causal_mask, layout, mesh, value_types, result_types):
  return _bwd_shardy_rule(len(value_types), has_dbias=False, is_fp8=True)

