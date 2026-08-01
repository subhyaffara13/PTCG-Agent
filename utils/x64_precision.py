
def x64_precision(enable_x64_precision: bool = True):
  """Context manager to temporarily enable x64 precision.

  Args:
    enable_x64_precision: Whether to enable or disable x64 precision within the
      context.

  Yields:
    None

  Examples:
    >>> from optax._src.utils import x64_precision
    >>> with x64_precision(enable_x64_precision=True):
    ...   print(jnp.float64(1.0).dtype.name)
    float64
    >>> with x64_precision(enable_x64_precision=False):
    ...   print(jnp.float64(1.0).dtype.name)
    float32
  """
  old_config = jax.config.jax_enable_x64
  try:
    jax.config.update('jax_enable_x64', enable_x64_precision)
    yield
  finally:
    jax.config.update('jax_enable_x64', old_config)

