
def _dot_product_attention_fp8_bwd_batcher(
    batched_args, batch_dims, *, scale, use_causal_mask, layout):
  _check_valid_batch_dims(batch_dims)
  query, key, value, fwd_output, grad_output, activation,\
    descale_q, descale_k, descale_v, descale_o, descale_dO, descale_s, descale_dP,\
    scale_s, scale_dQ, scale_dK, scale_dV, scale_dP = batched_args
  query_bdim = batch_dims[0]
  out_bdims = query_bdim, query_bdim, query_bdim

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

  activation = jnp.reshape(activation, (B, N, T))
  fwd_output = jnp.reshape(fwd_output, (B,) + query.shape[-3:])
  grad_output = jnp.reshape(grad_output, (B,) + query.shape[-3:])

  grads = _dot_product_attention_fp8_bwd_p_wrapper.bind(
      query, key, value, fwd_output, grad_output, activation,
      descale_q, descale_k, descale_v, descale_o, descale_dO, descale_s, descale_dP, scale_s, scale_dQ, scale_dK, scale_dV, scale_dP,
      scale=scale, use_causal_mask=use_causal_mask, layout=layout,
  )

  grad_query, grad_key, grad_value = grads[:3]
  # reshape to original shape
  grad_query = jnp.reshape(grad_query, query.shape)
  grad_key = jnp.reshape(grad_key, key.shape)
  grad_value = jnp.reshape(grad_value, value.shape)

  return grads, out_bdims

