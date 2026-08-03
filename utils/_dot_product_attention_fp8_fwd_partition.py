import functools

def _dot_product_attention_fp8_fwd_partition(
    scale, use_causal_mask, layout, is_training,
    mesh, arg_shapes, result_shape):
  # args sharding
  arg_shardings = tuple(arg_i.sharding for arg_i in arg_shapes)
  out_shardings = _infer_fp8_fwd_output_sharding(
    mesh, arg_shapes, is_training, layout)
  impl = functools.partial(
      _dot_product_attention_fp8_fwd_impl, scale=scale, use_causal_mask=use_causal_mask,
      layout=layout, is_training=is_training)
  return mesh, impl, out_shardings, arg_shardings

