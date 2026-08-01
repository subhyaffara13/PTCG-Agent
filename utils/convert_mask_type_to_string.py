
def convert_mask_type_to_string(mask_type: MaskType) -> str:
  if mask_type == MaskType.NO_MASK:
    return "NO_MASK"
  elif mask_type == MaskType.PADDING:
    return "PADDING"
  elif mask_type == MaskType.CAUSAL:
    return "CAUSAL"
  elif mask_type == MaskType.PADDING_CAUSAL:
    return "PADDING_CAUSAL"
  elif mask_type == MaskType.ALIBI:
    return "ALIBI"
  else:
    raise ValueError(f"Unexpected mask type: {mask_type}")

