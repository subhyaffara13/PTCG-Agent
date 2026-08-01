
def check_compute_capability(capability):
  if not 'cuda' in xla_bridge.get_backend().platform_version:
    return False
  d, *_ = xla_bridge.local_devices(backend="gpu")
  target = tuple(int(x) for x in capability.split("."))
  current = tuple(int(x) for x in d.compute_capability.split("."))
  return current >= target

