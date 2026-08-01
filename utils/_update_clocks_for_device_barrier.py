
def _update_clocks_for_device_barrier(token, device_id: jax.Array):
  device_id_as_int = int(device_id)
  del device_id

  shared_memory = _get_shared_memory()
  shared_memory.update_clocks_for_device_barrier(device_id_as_int)
  return token


def _update_clocks_for_device_barrier(token, device_id):
  """Synchronizes the vector clocks for the cores on the given device."""
  shared_memory = _get_shared_memory()
  shared_memory.update_clocks_for_device_barrier(device_id)
  return token

