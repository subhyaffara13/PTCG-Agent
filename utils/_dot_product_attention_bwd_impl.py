
def _dot_product_attention_bwd_impl(
    query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
    page_table_k, page_table_v, activation, fwd_output, grad_output, scale,
    seed, dropout_rate, variadic_args, mask_type, layout, sliding_window_length):
  q_seqlen, kv_seqlen, q_offsets, kv_offsets = \
      _fix_seqlen_offsets(q_seqlen, kv_seqlen, q_offsets, kv_offsets, query, key)
  grads = _dot_product_attention_bwd_p.bind(
      query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
      page_table_k, page_table_v, activation, fwd_output, grad_output,
      scale=scale, seed=seed,
      dropout_rate=dropout_rate, variadic_args=variadic_args,
      mask_type=mask_type, layout=layout,
      sliding_window_length=sliding_window_length)
  return grads

