
def is_tpu_device() -> bool:
  return chip_version_from_device_kind(get_device_kind()) is not None

