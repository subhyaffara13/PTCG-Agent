
def _device_identity_key(device: jax.Device) -> tuple[int, int, str]:
  """Returns a stable key for deduping devices across backend scans."""
  return (id(device.client), device.id, _device_platform(device))

