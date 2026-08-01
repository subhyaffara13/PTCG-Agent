
def debug_checks_enabled() -> bool:
  """Returns runtime checks are enabled."""
  return config.jax_pallas_enable_debug_checks.value

