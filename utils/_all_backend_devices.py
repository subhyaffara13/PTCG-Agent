
def _all_backend_devices() -> tuple[jax.Device, ...]:
  """Returns all devices visible to colocated-python serialization backends."""
  devices_by_key: dict[tuple[int, int, str], jax.Device] = {}

  local_devices = cp_serialization.xb.local_devices()
  if local_devices:
    # `local_devices()[0]` is only used to reach the default backend client;
    # `_get_all_devices()` then enumerates every device owned by that client.
    default_backend_client = local_devices[0].client
    for device in default_backend_client._get_all_devices():  # pylint: disable=protected-access
      devices_by_key.setdefault(_device_identity_key(device), device)

  for backend in cp_serialization.xb.backends().values():
    for device in backend._get_all_devices():  # pylint: disable=protected-access
      devices_by_key.setdefault(_device_identity_key(device), device)
  return tuple(devices_by_key.values())

