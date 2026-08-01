
def _dot_product_attention_core(query, key, value, bias, mask, is_causal,
                                scale, q_seqlen, kv_seqlen, local_window_size,
                                return_residual):
  logits_dtype = jnp.promote_types(query.dtype, np.float32)

  # If the query and logits dtypes are different, then the default precision
  # can use inconsistent types in the backwards pass
  # (see https://github.com/jax-ml/jax/issues/24047).
  if query.dtype == dtypes.bfloat16:
    precision = lax.DotAlgorithmPreset.BF16_BF16_F32
  elif query.dtype == np.float16:
    precision = lax.DotAlgorithmPreset.F16_F16_F32
  # TODO(sbodenstein): Implement this fix for all dtypes.
  else:
    precision = None

  # Explicit precision will fail on platforms that don't support it. For example,
  # some GPUs do not support BF16_BF16_F32, and TPU does not support F16_F16_F32.
  # Use the default precision as a fallback in these cases.
  try:
    logits = jnp_einsum.einsum(
        "BTNH,BSNH->BNTS",
        query,
        key,
        precision=precision,
        preferred_element_type=logits_dtype,
    )
  except:
    logits = jnp_einsum.einsum(
        "BTNH,BSNH->BNTS",
        query,
        key,
        precision=None,
        preferred_element_type=logits_dtype,
    )

  logits *= jnp.array(scale, dtype=logits.dtype)

  if bias is not None:
    logits = (logits + bias).astype(logits.dtype)

  padded_logits = _apply_masks(logits, mask, is_causal, q_seqlen, kv_seqlen,
                               local_window_size)

  # Softmax and it is always carried out in fp32.
  padded_logits = padded_logits.astype(np.float32)
  probs = softmax(padded_logits, axis=-1).astype(key.dtype)

  encoded = jnp_einsum.einsum('BNTS,BSNH->BTNH', probs, value)
  if q_seqlen is not None:
    mask = _get_padding_mask_encoded(encoded.shape[1], q_seqlen)
    encoded *= mask.astype(encoded.dtype)

  if return_residual:
    lse_residual = logsumexp(padded_logits, axis=-1).astype(key.dtype)
    lse_residual = jnp.transpose(lse_residual, (0, 2, 1))  # B N T -> B T N
    return encoded, lax.stop_gradient(lse_residual)

  return encoded

