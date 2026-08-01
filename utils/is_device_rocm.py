
def is_device_rocm() -> bool:
  return 'rocm' in xla_bridge.get_backend().platform_version

