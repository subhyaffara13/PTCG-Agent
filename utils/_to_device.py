
def _to_device(
    device: torch.device,
    dtype: torch.dtype,
    non_blocking: bool = False,
    copy: bool = False,
    memory_format: torch.memory_format | None = None,
) -> dict[str, Any]:
    kwargs = {
        "device": device,
        "dtype": dtype,
        "non_blocking": non_blocking,
        "copy": copy,
        "memory_format": memory_format,
    }
    return kwargs


def _to_device(device: DeviceType) -> torch.device:
    device = torch.device(device)
    if device.type != "cuda":
        raise ValueError(
            "`set_devices` expect a list of CUDA devices, but got "
            f"device type {device.type}."
        )
    return device


def _to_device(self: Array, device: xc.Device | Sharding, *,
               stream: int | Any | None = None):
  """Return a copy of the array on the specified device

  Args:
    device: :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.
    stream: not implemented, passing a non-None value will lead to an error.
  Returns:
    copy of array placed on the specified device or devices.
  """
  if stream is not None:
    raise NotImplementedError("stream argument of array.to_device()")
  return api.device_put(self, device)

