
def _dot_product_attention_fp8_fwd_abstract(
    query, key, value,
    descale_q, descale_k, descale_v, descale_s, scale_s, scale_o,
    scale, use_causal_mask, layout, is_training):
  if layout == AttentionLayout.BNTH.value:
    B, N, T, _ = query.shape
    _, _, S, _ = key.shape
  else:
    B, T, N, _ = query.shape
    _, S, _, _ = key.shape
  output_shape = query.shape
  softmax_stat_shape = (B, N, T)

  # output, amax_s, amax_o[, softmax_stat]
  if is_training:
    return (
      _attention_out_aval(query, output_shape),
      core.ShapedArray((1,1,1,1), np.float32),
      core.ShapedArray((1,1,1,1), np.float32),
      _attention_out_aval(query, softmax_stat_shape, np.float32),
    )
  else:
    return (
      _attention_out_aval(query, output_shape),
      core.ShapedArray((1,1,1,1), np.float32),
      core.ShapedArray((1,1,1,1), np.float32),
    )

