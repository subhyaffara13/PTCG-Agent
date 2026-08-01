
def is_torch_xla_available(check_is_tpu=False, check_is_gpu=False) -> bool:
    """
    Check if `torch_xla` is available. To train a native pytorch job in an environment with torch xla installed, set
    the USE_TORCH_XLA to false.
    """
    assert not (check_is_tpu and check_is_gpu), "The check_is_tpu and check_is_gpu cannot both be true."

    torch_xla_available = USE_TORCH_XLA in ENV_VARS_TRUE_VALUES and _is_package_available("torch_xla")[0]
    if not torch_xla_available:
        return False

    import torch_xla

    if check_is_gpu:
        return torch_xla.runtime.device_type() in ["GPU", "CUDA"]
    elif check_is_tpu:
        return torch_xla.runtime.device_type() == "TPU"

    return True

