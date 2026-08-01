
def is_mamba_2_ssm_available() -> bool:
    is_available, mamba_ssm_version = _is_package_available("mamba_ssm", return_version=True)
    return is_torch_cuda_available() and is_available and version.parse(mamba_ssm_version) >= version.parse("2.0.4")

