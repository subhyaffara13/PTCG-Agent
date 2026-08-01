
def _get_large_negative(dtype):
  dtype_max = dtypes.finfo(dtype).max
  # Softmax is always computed in float32 (see _dot_product_attention_core).
  # Cap at float32 range so that the large negative value stays finite when
  # cast to float32; otherwise float64 values would overflow to -inf and
  # trigger FloatingPointError under jax.debug_infs(True).
  dtype_max = min(dtype_max, dtypes.finfo(np.float32).max)
  return jnp.asarray(-0.7 * dtype_max, dtype=dtype)

