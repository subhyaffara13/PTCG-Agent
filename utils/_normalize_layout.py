
def _normalize_layout(layout: str) -> AttentionLayout:
  layout_upper = layout.upper()
  if layout_upper in ["BSNH", "BNSH", "BTNH", "BNTH"]:
    return AttentionLayout[layout_upper.replace("S", "T")]
  else:
    raise ValueError(f"Unsupported qkv_layout: {layout}")

