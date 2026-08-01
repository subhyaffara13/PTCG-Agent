
def _serialize_abstract_device(builder: flatbuffers.Builder,
                               device: mesh.AbstractDevice | None) -> int:
  if device is None:
    return 0
  device_kind = builder.CreateString(device.device_kind)
  platform = builder.CreateString(device.platform)

  ser_flatbuf.AbstractDeviceStart(builder)
  ser_flatbuf.AbstractDeviceAddDeviceKind(builder, device_kind)
  if device.num_cores is not None:
    ser_flatbuf.AbstractDeviceAddNumCores(builder, device.num_cores)
  ser_flatbuf.AbstractDeviceAddPlatform(builder, platform)
  return ser_flatbuf.AbstractDeviceEnd(builder)

