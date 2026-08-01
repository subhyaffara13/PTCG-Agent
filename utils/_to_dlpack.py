
def _to_dlpack(x: Array, stream: int | Any | None,
               src_device: _jax.Device | None = None,
               device: _jax.Device | None = None,
               copy: bool | None = None):

  if src_device is None:
    src_device, = x.devices()
  if device and (src_device is None or device != src_device):
    if copy is not None and not copy:
      raise ValueError(
        f"Specified {device=} which requires a copy since the source device "
        f"is {repr(src_device)}, however copy=False. Set copy=True or "
        "copy=None to perform the requested operation."
      )
    else:
      arr = device_put(x, device)
  else:
    arr = _array_copy(x) if copy else x
  return _jax.buffer_to_dlpack_managed_tensor(
    arr.addressable_data(0), stream=stream
  )

