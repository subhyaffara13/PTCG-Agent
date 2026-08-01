
def is_causal_conv1d_available() -> bool:
    return is_torch_cuda_available() and _is_package_available("causal_conv1d")[0]

