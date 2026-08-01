
def is_pytorch_quantization_available() -> bool:
    return _is_package_available("pytorch_quantization")[0]

