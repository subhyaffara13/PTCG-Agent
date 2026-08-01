
def _get_device_worker_key(device: jax.Device) -> tuple[int, ...]:
  """Returns a tuple uniquely identifying the worker/VM for `device`."""
  task_index = _get_device_task_index(device)
  slice_index = _get_device_slice_index(device)

  if task_index is not None and slice_index is not None:
    return (task_index, slice_index)
  if task_index is not None:
    return (task_index,)
  if slice_index is not None:
    msg = (
        'Pathways worker-key inference requires a task identifier; '
        'slice_index alone is ambiguous:'
        f' {device!r}'
    )
    logging.error(msg)
    raise ValueError(msg)

  msg = (
      'Unable to infer Pathways worker key from device attributes/repr:'
      f' {device!r}'
  )
  logging.error(msg)
  raise ValueError(msg)

