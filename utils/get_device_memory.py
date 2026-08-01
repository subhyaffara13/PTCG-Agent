
def get_device_memory() -> int:
  """Returns HBM capacity of the device on which the code is running(in bytes)."""
  device = jax.local_devices()[0]
  if device.platform == 'cpu':
    page_size = os.sysconf('SC_PAGE_SIZE')
    phys_pages = os.sysconf('SC_PHYS_PAGES')
    return int(page_size * phys_pages)

  if device.platform not in ('tpu', 'gpu'):
    raise ValueError('Only select TPU and GPU devices are supported.')

  return device.memory_stats()['bytes_limit']

