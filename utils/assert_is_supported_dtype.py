
def assert_is_supported_dtype(dtype: jnp.dtype) -> None:
  if dtype != jnp.bfloat16 and dtype != jnp.float32:
    raise ValueError(f"Expected bfloat16 or float32 array but got {dtype}.")

