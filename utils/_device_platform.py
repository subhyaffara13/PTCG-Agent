
def _device_platform(device: jax.Device) -> str:
  platform = getattr(device, 'platform', None)
  if platform is not None:
    return str(platform)
  return str(getattr(device, 'device_kind', 'unknown')).lower()

