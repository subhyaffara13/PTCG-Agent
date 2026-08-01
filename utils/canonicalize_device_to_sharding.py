
def canonicalize_device_to_sharding(device: xc.Device | Sharding | None
                                    ) -> Sharding | None:
  if isinstance(device, xc.Device):
    return make_single_device_sharding(device)
  return device

