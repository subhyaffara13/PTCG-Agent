from typing import Any

def _style_dict_to_str(style_dict: dict[str, Any]) -> str:
  return " ".join([f"{k}: {v};" for k, v in style_dict.items()])

