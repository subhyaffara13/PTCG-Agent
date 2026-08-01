
def _extract_pjrt_ifrt_device_id(device: jax.Device) -> int | None:
  """Returns the backend-global IFRT CPU id when the backend exposes one.

  Pathways sidecars log CPU devices like:

    `CpuDevice(id=0)[PjRtIFRTDeviceId=120]`

  where `device.id` is local to the remote-Python CPU backend, but the IFRT id
  is the backend-global id that matches controller-side specialization.

  Example:
  - controller serializes a CPU mesh using device id `120`
  - worker Python only exposes local ids `0..3`
  - the same worker device prints as `CpuDevice(id=0)[PjRtIFRTDeviceId=120]`

  JAX does not currently expose that backend-global id as a public Python
  attribute, so Orbax has to parse the repr while waiting for an upstream
  serialization fix.

  Args:
    device: The JAX device to extract the backend-global IFRT ID from.

  Returns:
    The integer PjRt IFRT device ID if present in the repr, otherwise None.
  """
  match = _PJRT_IFRT_DEVICE_ID_RE.search(repr(device))
  if not match:
    return None
  return int(match.group(1))

