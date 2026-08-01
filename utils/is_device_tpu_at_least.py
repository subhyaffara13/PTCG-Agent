
def is_device_tpu_at_least(version: int) -> bool:
  if device_under_test() != "tpu":
    return False
  return get_tpu_version() >= version

