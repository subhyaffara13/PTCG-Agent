
def _dot_product_attention_bwd_infer_sharding_from_operands(
    scale, seed, dropout_rate, variadic_args, mask_type, layout,
    sliding_window_length, mesh, arg_shapes, result_shape):
  return _infer_bwd_output_sharding(mesh, arg_shapes, layout, variadic_args)

