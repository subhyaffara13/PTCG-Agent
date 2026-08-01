
def _get_gpu_rtc_compatible_flags() -> list[str]:
    """
    Get HIPCC/NVCC flags that are compatible with NVRTC compilation.

    Returns:
        List of HIPCC/NVCC flags that can be safely used with NVRTC.
    """
    from torch.utils.cpp_extension import COMMON_HIPCC_FLAGS, COMMON_NVCC_FLAGS

    nvrtc_unsupported_flags = {
        "--expt-relaxed-constexpr",
    }

    # Filter out unsupported flags
    compatible_flags = [
        flag for flag in COMMON_NVCC_FLAGS if flag not in nvrtc_unsupported_flags
    ]

    if torch.version.hip:
        compatible_flags.extend(COMMON_HIPCC_FLAGS)

    return compatible_flags

