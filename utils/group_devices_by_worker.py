
def group_devices_by_worker(
    devices: Sequence[jax.Device],
) -> dict[tuple[int, ...], list[jax.Device]]:
  """Groups devices by their worker/VM.

  Pathways runtimes expose worker identity via device task/slice attributes
  because ``device.process_index`` is not unique per worker there.

  Args:
    devices: A sequence of JAX devices.

  Returns:
    A dict mapping worker keys to lists of devices belonging to that
    worker. Order is by first device occurrence.
  """
  worker_devices = collections.defaultdict(list)
  for d in devices:
    key = _get_device_worker_key(d)
    worker_devices[key].append(d)
  logging.vlog(
      1,
      'Grouped %d devices into %d Pathways workers: %s',
      len(devices),
      len(worker_devices),
      sorted(worker_devices),
  )
  return dict(worker_devices)

