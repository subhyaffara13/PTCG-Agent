
def _dot_product_attention(query: Array,
                           key: Array,
                           value: Array,
                           bias: Array,
                           q_seqlen: Array,
                           kv_seqlen: Array,
                           q_offsets: Array,
                           kv_offsets: Array,
                           page_table_k: Array,
                           page_table_v: Array,
                           scale: float,
                           seed: int,
                           dropout_rate: float,
                           variadic_args: tuple[bool, ...],
                           mask_type: bool,
                           layout: int,
                           sliding_window_length: int | None,
                           cudnn_version: int,
                           return_residual: bool):
  output = _dot_product_attention_fwd(
      query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
      page_table_k, page_table_v, scale=scale, seed=seed, dropout_rate=dropout_rate,
      variadic_args=variadic_args, mask_type=mask_type, layout=layout,
      sliding_window_length=sliding_window_length,
      cudnn_version=cudnn_version, return_residual=return_residual)
  return output

