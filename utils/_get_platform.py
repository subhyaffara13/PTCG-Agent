
def _get_platform(
    device_or_sharding: xc.Device | Sharding | None | str) -> str:
  """Get device_or_sharding platform or look up config.default_device.value."""
  if isinstance(device_or_sharding, xc.Device):
    return device_or_sharding.platform
  elif isinstance(device_or_sharding, Sharding):
    return list(device_or_sharding.device_set)[0].platform
  elif isinstance(device_or_sharding, str):
    return device_or_sharding
  elif device_or_sharding is None:
    if config.default_device.value is None:
      return xla_bridge.default_backend()
    else:
      return _get_platform(config.default_device.value)
  else:
    raise ValueError(f"`{device_or_sharding = }` was passed to"
                     "`canonicalize_or_get_default_platform`, only xc.Device,"
                     " Sharding, None or str values are supported.")

