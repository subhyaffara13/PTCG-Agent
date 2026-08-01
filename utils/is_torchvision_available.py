
def is_torchvision_available() -> bool:
    return is_vision_available() and is_torch_available() and _is_package_available("torchvision")[0]

