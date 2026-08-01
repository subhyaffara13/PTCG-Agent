
def _dot_product_attention_fp8_fwd_infer_sharding_from_operands(
    scale, use_causal_mask, layout, is_training,
    mesh, arg_shapes, result_shape):
  return _infer_fp8_fwd_output_sharding(mesh, arg_shapes, is_training, layout)

