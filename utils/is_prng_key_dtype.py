
def is_prng_key_dtype(dtype: jax.numpy.dtype | None) -> bool:
  """Returns True if the dtype is a PRNG key dtype (e.g. key<threefry2x32>)."""
  return dtype is not None and dtypes.issubdtype(dtype, dtypes.prng_key)

