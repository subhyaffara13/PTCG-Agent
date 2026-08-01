
def is_cuda_compute_capability_at_least(capability: str) -> bool:
  if not is_device_cuda():
    return False
  d, *_ = xla_bridge.local_devices(backend="gpu")
  target = tuple(int(x) for x in capability.split("."))
  current = tuple(int(x) for x in d.compute_capability.split("."))
  return current >= target

