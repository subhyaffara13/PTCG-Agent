
def _dot_product_attention_fwd_shardy_rule(
    scale, seed, dropout_rate, variadic_args, mask_type, layout, sliding_window_length,
    is_training, mesh, value_types, result_types):
  return _fwd_shardy_rule(value_types, result_types, layout, is_training, is_fp8=False)

