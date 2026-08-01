
def has_padding(mask_type: MaskType) -> bool:
  return mask_type == MaskType.PADDING or mask_type == MaskType.PADDING_CAUSAL

