
def is_torch_tensorrt_fx_available() -> bool:
    return _is_package_available("torch_tensorrt")[0] and _is_package_available("torch_tensorrt.fx")[0]

