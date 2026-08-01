
def _hash_devices(hash_obj, devices: np.ndarray) -> None:
  for device in devices.flat:
    _hash_string(hash_obj, device.device_kind)

