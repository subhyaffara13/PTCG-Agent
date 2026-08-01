
def _get_worker_count_key(device: jax.Device) -> tuple[tuple[int, ...], bool]:
  """Returns a best-effort worker key for `worker_count` compatibility."""
  attrs = []
  warn = False

  task_index = _get_device_task_index(device)
  if task_index is not None:
    attrs.append(task_index)
  else:
    warn = True

  slice_index = _get_device_slice_index(device)
  if slice_index is not None:
    attrs.append(slice_index)
  else:
    warn = True

  return tuple(attrs), warn

