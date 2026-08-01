
def select_input_dtype(lhs: jnp.ndarray, rhs: jnp.ndarray) -> jnp.dtype:
  """A type to which both input should be adapted to before dot product."""
  # bf16xbf16 matmul is only supported since TPUv4 generation. In case of mixed
  # input precision, we need to convert bf16 argument to fp32 beforehand.
  if (
      supports_bfloat16_matmul()
      and lhs.dtype == jnp.bfloat16
      and rhs.dtype == jnp.bfloat16
  ):
    return jnp.bfloat16
  else:
    return jnp.float32

