import math


def _dot_product_attention_fp8_fwd_batcher(
    batched_args, batch_dims, *, scale, use_causal_mask, layout, is_training):
  _check_valid_batch_dims(batch_dims)
  query, key, value,\
    descale_q, descale_k, descale_v, descale_s, scale_s, scale_o, = batched_args
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

  # reshape to 4D shape
  query = jnp.reshape(query, (B,) + query.shape[-3:])
  key = jnp.reshape(key, (B,) + key.shape[-3:])
  value = jnp.reshape(value, (B,) + key.shape[-3:])

  outputs = _dot_product_attention_fp8_fwd_p_wrapper.bind(
      query, key, value, descale_q, descale_k, descale_v, descale_s, scale_s, scale_o,
      scale=scale, use_causal_mask=use_causal_mask, layout=layout, is_training=is_training)

  # reshape to original shape
  output, amax_s, amax_o = outputs[0], outputs[1], outputs[2]
  output = jnp.reshape(output, query.shape)
  if is_training:
    activation = outputs[3]
    activation = jnp.reshape(activation, (*Bs, N, T))
    return (output, amax_s, amax_o, activation), out_bdims
  else:
    return (output, amax_s, amax_o), out_bdims

