
def is_fbgemm_gpu_available() -> bool:
    return _is_package_available("fbgemm_gpu")[0]

