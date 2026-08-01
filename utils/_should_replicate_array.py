
def _should_replicate_array(shape: tuple[int, ...]) -> bool:
  """Returns True if the array should be replicated across devices."""
  return len(shape) == 0 or shape[0] < jax.local_device_count()

