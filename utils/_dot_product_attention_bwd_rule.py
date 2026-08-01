
def _dot_product_attention_bwd_rule(
    scale, seed, dropout_rate, variadic_args, mask_type, layout,
    sliding_window_length, is_training, return_residual, res, grad_output):
  (query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
   page_table_k, page_table_v, activation, fwd_output) = res
  if return_residual:
    grad_output = grad_output[0]
  grads = _dot_product_attention_bwd_p_wrapper.bind(
      query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
      page_table_k, page_table_v, activation, fwd_output, grad_output,
      scale=scale, seed=seed, dropout_rate=dropout_rate, variadic_args=variadic_args,
      mask_type=mask_type, layout=layout,
      sliding_window_length=sliding_window_length
  )
  grads = (*grads,) + (None,) * (10 - len(grads))
  return grads

