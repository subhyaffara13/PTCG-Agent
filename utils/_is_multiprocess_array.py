
def _is_multiprocess_array(value: Any) -> bool:
  """Use GlobalAsyncCheckpointManager to save the array if it's only partially available on this host."""
  if isinstance(value, jax.Array):
    return not value.is_fully_addressable
  return False

