
def _dot_product_attention_fwd_infer_sharding_from_operands(
    scale, seed, dropout_rate, variadic_args, mask_type, layout, sliding_window_length,
    is_training, mesh, arg_shapes, result_shape):
  return _infer_fwd_output_sharding(mesh, arg_shapes, variadic_args, is_training, layout)

