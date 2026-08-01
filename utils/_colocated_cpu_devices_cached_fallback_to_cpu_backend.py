
def _colocated_cpu_devices_cached_fallback_to_cpu_backend(
    devices: tuple[jax.Device, ...],
) -> Sequence[jax.Device]:
  # TODO(hyeontaek): Remove this fallback path once a PjRt-IFRT backend defines
  # CPU devices by its own instead of using a separate CPU backend.
  if devices[0].device_kind == "cpu":
    # Use the devices from the backend of an original device if it defines CPU
    # devices.
    cpu_backend_devices = [d for d in devices[0].client._get_all_devices()
                           if d.device_kind == "cpu"]
  else:
    # PjRt-IFRT on a non-CPU platform currently defines CPU devices on a separae
    # CPU backend.
    cpu_backend_devices = jax.devices(backend="cpu")

  cpu_device_map = collections.defaultdict(list)
  for d in cpu_backend_devices:
    cpu_device_map[d.process_index].append(d)

  # Reverse each local CPU device list to make it cheaper to pop.
  for process_index in cpu_device_map.keys():
    cpu_device_map[process_index].reverse()

  cpu_devices = []
  for d in devices:
    try:
      cpu_devices.append(cpu_device_map[d.process_index].pop())
    except IndexError:
      raise ValueError(
          f"Process {d.process_index} does not have enough local CPU devices")
  return cpu_devices

