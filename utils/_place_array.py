
def _place_array(_arr, device, dlpack_device, copy):
  if device and dlpack_device != device:
    return device_put(_arr, device)
  if copy:
    return jnp.array(_arr, copy=True)
  return _arr

