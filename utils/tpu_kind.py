
def tpu_kind() -> str:
  """Query identification string for the currently attached TPU."""
  return jax.devices()[0].device_kind

