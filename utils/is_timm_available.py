
def is_timm_available() -> bool:
    return is_vision_available() and is_torch_available() and _is_package_available("timm")[0]

