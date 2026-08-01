
def get_tpu_info_for_chip(
    chip_version: ChipVersion, num_tensor_cores_per_logical_device: int
) -> TpuInfo:
  """Returns the TPU hardware info for the given TPU chip version.

  Note that all information is *per-TensorCore* so you would need to multiply by
  `num_tensor_cores_per_logical_device` to obtain the total for the chip.

  Args:
    chip_version: The TPU chip version.
    num_tensor_cores_per_logical_device: The number of TensorCores per logical
      device in the requested configuration. Should be 1 for single-core chips
      (TPU_V4I, TPU_V5E, TPU_V6E). For dual-core chips that support Megacore
      (TPU_V4, TPU_V5P), this can be 2 (Megacore mode) or 1 (split mode). For
      dual-core chips that do not support Megacore (TPU_V2, TPU_V3, TPU_7X),
      this must be 1.
  """
  if (
      chip_version.is_lite
      or chip_version
      in {
          ChipVersion.TPU_V2,
          ChipVersion.TPU_V3,
          ChipVersion.TPU_7,
          ChipVersion.TPU_7X,
          ChipVersion.TPU_8I,
      }
  ) and num_tensor_cores_per_logical_device != 1:
    raise ValueError(
        "Lite chips and dual-core chips that do not support Megacore must "
        "have num_tensor_cores_per_logical_device=1, but got"
        f" {num_tensor_cores_per_logical_device}."
    )

  return _get_tpu_info_impl(chip_version, num_tensor_cores_per_logical_device)

