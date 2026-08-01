
def _dot_product_attention_fwd_rule(
    query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
    page_table_k, page_table_v, scale, seed, dropout_rate, variadic_args,
    mask_type, layout, sliding_window_length, cudnn_version,
    return_residual):
  # check if flash attention is supported for this attention pattern
  check_is_flash_attention(
      query, key, value, layout, cudnn_version, bias is not None, True,
      get_max_seg_per_batch(q_offsets) > 1)
  outputs = _dot_product_attention_fwd_p_wrapper.bind(
      query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
      page_table_k, page_table_v, scale=scale, seed=seed, dropout_rate=dropout_rate,
      variadic_args=variadic_args, mask_type=mask_type, layout=layout,
      sliding_window_length=sliding_window_length, is_training=True)
  res = (query, key, value, bias, q_seqlen, kv_seqlen, q_offsets,
         kv_offsets, page_table_k, page_table_v, outputs[1], outputs[0])
  if return_residual:
    return tuple(outputs), res
  else:
    return outputs[0], res

