
def get_tpu_info() -> TpuInfo:
  """Returns the TPU hardware info for the current device.

  Note that all information is *per-TensorCore* so you would need to multiply by
  `num_cores` to obtain the total for the chip.
  """
  device_kind = get_device_kind()
  chip_version = chip_version_from_device_kind(device_kind)
  if chip_version is None:
    if device_kind in registry:
      return registry[device_kind]()
    raise ValueError(f"Unsupported TPU device kind: {device_kind}")
  return _get_tpu_info_impl(chip_version, get_num_device_cores())

