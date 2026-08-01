
def _dot_product_attention_fwd_partition(
    scale, seed, dropout_rate, variadic_args, mask_type, layout, sliding_window_length,
    is_training, mesh, arg_shapes, result_shape):
  # args sharding
  arg_shardings = tuple(arg_i.sharding for arg_i in arg_shapes)
  out_shardings = _infer_fwd_output_sharding(
    mesh, arg_shapes, variadic_args, is_training, layout)
  impl = functools.partial(
      _dot_product_attention_fwd_impl,
      scale=scale,
      seed=seed,
      dropout_rate=dropout_rate,
      variadic_args=variadic_args,
      mask_type=mask_type,
      layout=layout,
      sliding_window_length=sliding_window_length,
      is_training=is_training,
  )
  return mesh, impl, out_shardings, arg_shardings

