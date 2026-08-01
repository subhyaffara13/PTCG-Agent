
def _get_device_task_index(device: jax.Device) -> int | None:
  if (
      hasattr(device, 'virtual_task_index')
      and device.virtual_task_index is not None
  ):
    return int(device.virtual_task_index)
  task_index = _extract_int_from_repr(device, r'logical_task=(\d+)')
  if task_index is not None:
    return task_index
  if hasattr(device, 'task_id') and device.task_id is not None:
    return int(device.task_id)
  return _extract_int_from_repr(device, r'vtask=(\d+)')

