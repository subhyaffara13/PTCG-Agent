
def _dot_product_attention_bwd_abstract(
    query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
    page_table_k, page_table_v, activation, fwd_output, grad_output, *,
    scale, seed, dropout_rate, variadic_args, mask_type, layout, sliding_window_length):
  _, has_dbias = variadic_args
  if has_dbias:
    # cuDNN supports bias for this case
    return (
      _attention_out_aval(query),  # grad query
      _attention_out_aval(key),  # grad key
      _attention_out_aval(value),  # grad value
      _attention_out_aval(bias),  # grad bias
    )
  else:
    return (
      _attention_out_aval(query),  # grad query
      _attention_out_aval(key),  # grad key
      _attention_out_aval(value),  # grad value
    )

