
def count_internal_device_puts():
  before = _jaxlib._jax.get_internal_device_put_info()
  counts = {}
  try:
    yield lambda: counts
  finally:
    after = _jaxlib._jax.get_internal_device_put_info()
    for k, v in after.items():
      diff = v - before.get(k, 0)
      if diff != 0:
        counts[k] = diff

