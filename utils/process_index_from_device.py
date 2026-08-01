
def process_index_from_device(device: jax.Device) -> int:
  """Customized logic for obtaining JAX process index from a device."""
  if use_experimental_distributed_process_id():
    return runtime_to_distributed_process_id(device.process_index)
  else:
    return device.process_index

