
def _dot_product_attention_fwd_abstract(
    query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
    page_table_k, page_table_v, *, scale, seed, dropout_rate, variadic_args,
    mask_type, layout, sliding_window_length, is_training):
  if layout == AttentionLayout.BNTH.value:
    B, N, T, _ = query.shape
    _, _, S, H = value.shape
    output_shape = (B, N, T, H)
  else:
    B, T, N, _ = query.shape
    _, S, _, H = value.shape
    output_shape = (B, T, N, H)

  max_seg_per_batch = get_max_seg_per_batch(q_offsets)
  softmax_stat_shape = (B * max_seg_per_batch, N, T)

  if is_training:
    return (
      _attention_out_aval(query, output_shape),  # output
      _attention_out_aval(query, softmax_stat_shape, np.float32),  # softmax_stat
    )
  else:
    return (
      _attention_out_aval(query, output_shape),  # output
    )

