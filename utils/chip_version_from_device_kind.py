
def chip_version_from_device_kind(device_kind: str) -> ChipVersion | None:
  match device_kind:
    case "TPU v2":
      return ChipVersion.TPU_V2
    case "TPU v3":
      return ChipVersion.TPU_V3
    case "TPU v4":
      return ChipVersion.TPU_V4
    case "TPU v4 lite":
      return ChipVersion.TPU_V4I
    case "TPU v5e" | "TPU v5 lite":
      return ChipVersion.TPU_V5E
    case "TPU v5" | "TPU v5p":
      return ChipVersion.TPU_V5P
    case "TPU v6e" | "TPU v6 lite":
      return ChipVersion.TPU_V6E
    case "TPU7":
      return ChipVersion.TPU_7
    case "TPU7x":
      return ChipVersion.TPU_7X
    case "TPU8i":
      return ChipVersion.TPU_8I
    case _:
      return None

