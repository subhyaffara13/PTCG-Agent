
def _has_prng_key_dtype(arg: Any) -> bool:
  """Returns True if the dtype of arg is a PRNG key dtype."""
  return arg.dtype is not None and jax.dtypes.issubdtype(
      arg.dtype, jax.dtypes.prng_key
  )

