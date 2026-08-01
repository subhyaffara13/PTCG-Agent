
def check_device_backend_on_shardings(shardings) -> bool:
  for i in shardings:
    if isinstance(i, UnspecifiedValue):
      continue
    if getattr(i, '_device_backend', False):
      return True
  return False

