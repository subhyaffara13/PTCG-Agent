
def _deserialize_abstract_device(
    ser_abs_device: ser_flatbuf.AbstractDevice | None
    ) -> mesh.AbstractDevice | None:
  if ser_abs_device is None:
    return None
  device_kind = ser_abs_device.DeviceKind().decode("utf-8")
  num_cores: int | None = ser_abs_device.NumCores()
  if (platform := ser_abs_device.Platform()):
    platform = platform.decode("utf-8")
  else:
    platform = get_platform_from_device_kind(device_kind)
  return mesh.AbstractDevice(device_kind, num_cores, platform)

