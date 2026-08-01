
def is_bf16_supported(including_emulation: bool = True):
    r"""Return a bool indicating if the current CUDA/ROCm device supports dtype bfloat16."""
    # Check for ROCm, if true return true, no ROCM_VERSION check required,
    # since it is supported on AMD GPU archs.
    if torch.version.hip:
        return True

    # If CUDA is not available, than it does not support bf16 either
    if not is_available():
        return False

    device = torch.cuda.current_device()

    if torch.cuda.get_device_properties(device).major >= 8:
        return True

    if not including_emulation:
        return False

    # Finally try to create a bfloat16 device.
    return _check_bf16_tensor_supported(device)


def is_bf16_supported(including_emulation: bool = True):
    r"""Return a bool indicating if the current MTIA device supports dtype bfloat16."""
    return True


def is_bf16_supported(including_emulation: bool = True) -> bool:
    r"""Return a bool indicating if the current XPU device supports dtype bfloat16."""
    if not is_available():
        return False
    return (
        including_emulation
        or torch.xpu.get_device_properties().has_bfloat16_conversions
    )

