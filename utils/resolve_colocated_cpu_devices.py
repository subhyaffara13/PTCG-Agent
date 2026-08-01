
def resolve_colocated_cpu_devices(
    device_ids: Sequence[int],
) -> tuple[jax.Device, ...]:
  """Resolves controller-visible colocated CPU ids on the worker backend.

  Args:
    device_ids: A sequence of logical Pathways device IDs.

  Returns:
    A tuple of corresponding JAX CPU devices.

  Raises:
    ValueError: If device_ids contains CPU devices not visible to sidecar.
  """
  cpu_device_map = _get_cpu_device_map()
  missing_ids = [
      device_id for device_id in device_ids if device_id not in cpu_device_map
  ]
  if missing_ids:
    raise ValueError(
        'mesh_device_ids contains CPU devices not visible to the sidecar: '
        f'{missing_ids}.'
    )
  return tuple(cpu_device_map[device_id] for device_id in device_ids)

