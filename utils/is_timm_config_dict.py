from typing import Any

def is_timm_config_dict(config_dict: dict[str, Any]) -> bool:
    """Checks whether a config dict is a timm config dict."""
    return "pretrained_cfg" in config_dict

