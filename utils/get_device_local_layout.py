
def get_device_local_layout(arr: jax.Array) -> Any:
  """Returns device_local_layout of a jax.Array."""
  return (
      arr.format.layout  # pytype: disable=attribute-error
      if jax.__version_info__ >= (0, 6, 3)
      else arr.format.device_local_layout  # pytype: disable=attribute-error
  )

