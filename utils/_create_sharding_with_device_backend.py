
def _create_sharding_with_device_backend(device, backend):
  if device is not None:
    assert backend is None
    out = make_single_device_sharding(device)
  elif backend is not None:
    assert device is None
    out = make_single_device_sharding(
        xb.get_backend(backend).local_devices()[0])
  else:
    raise AssertionError('Unreachable!')
  out._device_backend = True
  return out

