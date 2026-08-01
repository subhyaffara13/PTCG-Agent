
def _get_current_shard_shape(shape: tuple[int, ...]) -> tuple[int, ...]:
  """Calculates current shard shape."""
  num_devices_per_host = jax.local_device_count()

  if _should_replicate_array(shape):
    return (1,) + shape
  else:
    shard_size = shape[0] // num_devices_per_host
    return (1, shard_size) + shape[1:]

