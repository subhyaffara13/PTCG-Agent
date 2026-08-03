import math


def _dot_product_attention_bwd_batcher(
     batched_args, batch_dims, *, scale, seed, dropout_rate, variadic_args,
     mask_type, layout, sliding_window_length):
  _check_valid_batch_dims(batch_dims)
  query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets, \
    page_table_k, page_table_v, activation, fwd_output, grad_output = batched_args
  query_bdim = batch_dims[0]
  out_bdims = query_bdim, query_bdim, query_bdim

  if layout == AttentionLayout.BNTH.value:
    *Bs, N, T, _ = query.shape
    *_, _, S, _ = key.shape
  else:
    *Bs, T, N, _ = query.shape
    *_, S, _, _ = key.shape
  B = math.prod(Bs)
  has_bias, has_dbias = variadic_args
  original_query_shape = query.shape
  original_key_shape = key.shape
  original_value_shape = value.shape
  original_bias_shape = bias.shape if has_bias else None
  # reshape to 4D shape
  query = jnp.reshape(query, (B,) + query.shape[-3:])
  key = jnp.reshape(key, (B,) + key.shape[-3:])
  value = jnp.reshape(value, (B,) + key.shape[-3:])
  if has_bias and batch_dims[3] is not None:
    bias = jnp.reshape(bias, (B, N, T, S))
  if has_padding(mask_type):
    q_seqlen = jnp.reshape(q_seqlen, (B, ))
    kv_seqlen = jnp.reshape(kv_seqlen, (B, ))

  activation = jnp.reshape(activation, (B, N, T))
  fwd_output = jnp.reshape(fwd_output, (B,) + query.shape[-3:])
  grad_output = jnp.reshape(grad_output, (B,) + query.shape[-3:])

  grads = _dot_product_attention_bwd_p_wrapper.bind(
      query, key, value, bias, q_seqlen, kv_seqlen, q_offsets, kv_offsets,
      page_table_k, page_table_v, activation, fwd_output, grad_output,
      scale=scale, seed=seed, dropout_rate=dropout_rate, variadic_args=variadic_args,
      mask_type=mask_type, layout=layout,
      sliding_window_length=sliding_window_length,
  )

  # reshape to original shape
  grads[0] = jnp.reshape(grads[0], original_query_shape)
  grads[1] = jnp.reshape(grads[1], original_key_shape)
  grads[2] = jnp.reshape(grads[2], original_value_shape)
  if has_dbias:
    assert has_bias
    if variadic_args[1]:
      grads[3] = jnp.reshape(grads[3], original_bias_shape)
    else:
      grads.append(jnp.zeros(original_bias_shape, bias.dtype))
    out_bdims += (batch_dims[3],)
  return grads, out_bdims

