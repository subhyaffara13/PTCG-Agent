
def is_mamba_ssm_available() -> bool:
    return is_torch_cuda_available() and _is_package_available("mamba_ssm")[0]

