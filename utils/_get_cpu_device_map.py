
def _get_cpu_device_map() -> Mapping[int, jax.Device]:
  """Builds a worker-side CPU lookup for JAX colocated deserialization.

  JAX calls this while unreducing every colocated `Mesh`, `DeviceList`, or
  `SingleDeviceSharding`. Backend device topology is stable for this process,
  so the map is cached to avoid repeated backend scans.

  The controller serializes colocated CPU objects by controller-visible
  `device.id`, which is a backend-global IFRT id in the Pathways runtime. The
  worker-side remote-Python CPU backend can expose different local `device.id`
  values, so we first register the backend-global IFRT id parsed from repr and
  then fall back to the local `device.id` without overwriting the global entry.

  When the IFRT id and local `device.id` namespaces do not collide, this keeps
  both lookups working. If the namespaces collide for different devices, the
  map is ambiguous and this function fails instead of returning the wrong CPU.
  """
  cpu_device_map: dict[int, jax.Device] = {}
  backend_devices = _all_backend_devices()
  for device in backend_devices:
    if _device_platform(device) != 'cpu':
      continue
    ifrt_device_id = _extract_pjrt_ifrt_device_id(device)
    if ifrt_device_id is None:
      continue
    existing = cpu_device_map.get(ifrt_device_id)
    if existing is not None and existing != device:
      raise ValueError(
          'Multiple CPU devices with PjRt-IFRT id '
          f'{ifrt_device_id} found: {existing} and {device}'
      )
    cpu_device_map[ifrt_device_id] = device

  for device in backend_devices:
    if _device_platform(device) != 'cpu':
      continue
    existing = cpu_device_map.get(device.id)
    if existing is not None and existing != device:
      raise ValueError(
          'CPU device id '
          f'{device.id} is ambiguous: it is both a PjRt-IFRT id for '
          f'{existing} and a local device id for {device}'
      )
    if existing is None:
      cpu_device_map[device.id] = device

  return types.MappingProxyType(cpu_device_map)


def _get_cpu_device_map() -> dict[int, jax.Device]:
  """Returns a map from a device id to a matching device."""
  cpu_device_map: dict[int, jax.Device] = {}
  # TODO(hyeontaek): We should look up CPU devices for a specific CPU backend.
  # When deserializing a device on the controller, the backend should be the one
  # associated with colocated_python. When deserializing on the colocated_python
  # executor, it should be the CPU backend visible to the user function running
  # under colocated_python.

  # Look for CPU devices in the default backend.
  for d in xb.local_devices()[0].client._get_all_devices():
    if d.device_kind == "cpu":
      if d.id in cpu_device_map:
        raise ValueError(
            f"Multiple CPU devices with id {d.id} found:"
            f" {cpu_device_map[d.id]} and {d}"
        )
      cpu_device_map[d.id] = d
  if cpu_device_map:
    return cpu_device_map

  # Fall back to searching CPU devices in all backends.
  for backend in xb.backends().values():
    for d in backend._get_all_devices():
      if d.device_kind == "cpu":
        if d.id in cpu_device_map:
          raise ValueError(
              f"Multiple CPU devices with id {d.id} found:"
              f" {cpu_device_map[d.id]} and {d}"
          )
        cpu_device_map[d.id] = d
  return cpu_device_map

