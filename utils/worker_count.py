
def worker_count(global_mesh: jax.sharding.Mesh | None) -> int:
  """Gets the number of Pathways workers.

  Args:
    global_mesh: The global mesh of active devices. If None is provided,
      `jax.devices()` will be used.

  Returns:
    The number of Pathways workers in the mesh.
  """
  global_mesh = global_mesh or jax.sharding.Mesh(jax.devices(), 'x')
  devices = global_mesh.devices.flatten()
  workers = set()
  warn = False
  for d in devices:
    worker_key, missing_metadata = _get_worker_count_key(d)
    workers.add(worker_key)
    warn = warn or missing_metadata

  if warn:
    logging.warning(
        'worker_count() may not be accurate; task or slice metadata was '
        'missing from some Pathways devices: %s',
        devices,
    )
  return len(workers)

