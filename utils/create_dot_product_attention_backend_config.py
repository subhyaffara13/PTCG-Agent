
def create_dot_product_attention_backend_config(
    batch,
    num_heads,
    seq_q,
    seq_kv,
    dtype,
    fmha_scale,
    seed,
    dropout_rate,
    mask_type,
    layout,
    sliding_window_length,
    max_seg_per_batch,
    is_paged_attention,
    is_bwd
):
  backend_config = create_dot_product_attention_backend_config_base(
      batch, num_heads, seq_q, seq_kv, dtype,
      fmha_scale, mask_type, layout, is_bwd
  )
  if sliding_window_length is None:
    sliding_window_length = 0
  backend_config['cudnn_fmha_backend_config']["dropout_rate"] = dropout_rate
  backend_config['cudnn_fmha_backend_config']["seed"] = seed
  backend_config['cudnn_fmha_backend_config']["sliding_window_length"] = sliding_window_length
  backend_config['cudnn_fmha_backend_config']["max_seg_per_batch"] = max_seg_per_batch
  backend_config['cudnn_fmha_backend_config']["is_paged_attention"] = is_paged_attention
  return json.dumps(backend_config)

