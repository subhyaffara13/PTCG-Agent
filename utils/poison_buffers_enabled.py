
def poison_buffers_enabled() -> bool:
  """Returns whether Pallas buffer poisoning is enabled."""
  return config.jax_pallas_poison_buffers.value

