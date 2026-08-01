
def _dot_product_attention_fwd_batcher(
    batched_args, batch_dims, *, scale, seed, dropout_rate, variadic_args,
    mask_type, layout, sliding_window_length, is_training):
  _check_valid_batch_dims(batch_dims)
  query, key, value, bias, q_seqlen, kv_seqlen, \
    q_offsets, kv_offsets, page_table_k, page_table_v = batched_args
  query_bdim = batch_dims[0]
  if is_training:
    out_bdims = query_bdim, query_bdim
  else:
    out_bdims = (query_bdim,)

  if layout == AttentionLayout.BNTH.value:
    *Bs, N, T, _ = query.shape
    *_, _, S, _ = key.shape
  else:
    *Bs, T, N, _ = query.shape
    *_, S, _, _ = key.shape
  B = math.prod(Bs)
  has_bias, _ = variadic_args
  original_shape = query.shape
  # reshape to 4D shape
  query = jnp.reshape(query, (B,) + query.shape[-3:])
  key = jnp.reshape(key, (B,) + key.shape[-3:])
  value = jnp.reshape(value, (B,) + key.shape[-3:])
  if has_bias and batch_dims[3] is not None:
    bias = jnp.reshape(bias, (B, N, T, S))
  if has_padding(mask_type):
    q_seqlen = jnp.reshape(q_seqlen, (B, ))
    kv_seqlen = jnp.reshape(kv_seqlen, (B, ))

  outputs = _dot_product_attention_fwd_p_wrapper.bind(
      query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
      page_table_k, page_table_v, scale=scale, seed=seed, dropout_rate=dropout_rate,
      variadic_args=variadic_args, mask_type=mask_type, layout=layout,
      sliding_window_length=sliding_window_length, is_training=is_training)

  # reshape to original shape
  output = outputs[0]
  output = jnp.reshape(output, original_shape)
  if is_training:
    activation = outputs[1]
    activation = jnp.reshape(activation, (*Bs, N, T))
    return (output, activation), out_bdims
  else:
    return (output,), out_bdims

