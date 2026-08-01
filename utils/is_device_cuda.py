
def is_device_cuda() -> bool:
  return 'cuda' in xla_bridge.get_backend().platform_version

