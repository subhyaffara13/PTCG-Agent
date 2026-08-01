
def _colocated_cpu_devices_cached(
    devices: tuple[jax.Device, ...],
) -> Sequence[jax.Device]:
  cpu_devices_by_colocation_id = collections.defaultdict(list)
  for device in devices[0].client._get_all_devices():
    if device.device_kind == "cpu":
      cpu_devices_by_colocation_id[device.colocation_id].append(device)
  if not cpu_devices_by_colocation_id:
    raise ValueError("No CPU devices found")

  colocated_cpu_devices = []
  for device in devices:
    matches = cpu_devices_by_colocation_id[device.colocation_id]
    if not matches:
      raise ValueError(f"Device {device} has no colocated devices")
    elif len(matches) > 1:
      raise ValueError(
          f"Ambiguous colocated devices; device {device} has"
          f" {len(matches)} colocated devices: f{matches}"
      )
    colocated_cpu_devices.append(matches[0])
  return colocated_cpu_devices

