
def unique_colocated_cpu_devices(
    devices: Sequence[jax.Device],
) -> tuple[jax.Device, ...]:
  """Returns colocated CPU devices with duplicate CPU ids removed."""
  all_cpu = tuple(cp.colocated_cpu_devices(tuple(devices)))
  unique_cpu = []
  seen_ids = set()
  for device in all_cpu:
    if device.id in seen_ids:
      continue
    seen_ids.add(device.id)
    unique_cpu.append(device)
  return tuple(unique_cpu)

