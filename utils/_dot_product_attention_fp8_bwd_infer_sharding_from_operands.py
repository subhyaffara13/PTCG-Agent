
def _dot_product_attention_fp8_bwd_infer_sharding_from_operands(
    scale, use_causal_mask, layout, mesh,
    arg_shapes, result_shape):
  return _infer_fp8_bwd_output_sharding(mesh, arg_shapes, layout)

