
def _dot_product_attention_xla(
    query: Array,
    key: Array,
    value: Array,
    bias: Array | None,
    mask: Array | None,
    is_causal: bool,
    scale: float,
    q_seqlen: Array | None,
    kv_seqlen: Array | None,
    local_window_size: tuple[int, int] | None,
    return_residual: bool = False):

  B, T, N, H = query.shape
  _, S, K, _ = key.shape
  G = N // K

  query = jnp.reshape(query, (B, T, K, G, H))
  def _reshape_to_grouped(t):
    if t is not None:
      tB, tN, tT, tS = t.shape
      if tN == 1:
        t = jnp.broadcast_to(t[:, :, None, :, :], (tB, tN, G, tT, tS))
      else:
        assert tN == N
        t = jnp.reshape(t, (tB, K, G, tT, tS))
    return t
  bias = _reshape_to_grouped(bias)
  mask = _reshape_to_grouped(mask)
  vmapped_fn = api.vmap(
      _dot_product_attention_core,
      in_axes=(3, None, None, 2, 2, None, None, None, None, None, None),
      out_axes=3,
  )
  output = vmapped_fn(query, key, value, bias, mask, is_causal, scale,
                       q_seqlen, kv_seqlen, local_window_size, return_residual)

  if return_residual:
    encoded, lse_residual = output
    encoded = jnp.reshape(encoded, (B, T, N, H))
    lse_residual = jnp.reshape(lse_residual, (B, T, N))
    return encoded, lse_residual

  encoded = jnp.reshape(output, (B, T, N, H))
  return encoded

