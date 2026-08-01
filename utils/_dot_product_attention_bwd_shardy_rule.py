
def _dot_product_attention_bwd_shardy_rule(
    scale, seed, dropout_rate, variadic_args,
    mask_type, layout, sliding_window_length, mesh, value_types, result_types):
  _, has_dbias = variadic_args
  return _bwd_shardy_rule(len(value_types), has_dbias, is_fp8=False)

