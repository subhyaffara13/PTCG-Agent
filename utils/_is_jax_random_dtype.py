
def _is_jax_random_dtype(dtype: Any) -> bool:
  return lazy.has_jax and isinstance(dtype, lazy.jax._src.prng.KeyTy)  # pylint: disable=protected-access

