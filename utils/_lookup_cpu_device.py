
def _lookup_cpu_device(
    cpu_device_map: dict[int, jax.Device], device_id: int
) -> jax.Device:
  """Returns a CPU device with the given device ID."""
  d = cpu_device_map.get(device_id)
  if d is None:
    raise ValueError(
        f"Invalid device ID {device_id}. Device list must contain only CPU"
        " devices."
    )
  return d

