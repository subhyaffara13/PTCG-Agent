import functools

def _dot_product_attention_fp8_bwd_partition(
    scale, use_causal_mask, layout, mesh,
    arg_shapes, result_shape):
  out_shardings = _infer_fp8_bwd_output_sharding(mesh, arg_shapes, layout)
  # args sharding
  arg_shardings = tuple(arg_i.sharding for arg_i in arg_shapes)
  impl = functools.partial(
      _dot_product_attention_fp8_bwd_impl, scale=scale,
      use_causal_mask=use_causal_mask, layout=layout
  )
  return mesh, impl, out_shardings, arg_shardings

