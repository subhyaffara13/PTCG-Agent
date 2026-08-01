
def is_tf32_supported() -> bool:
    r"""Return a bool indicating if the current CUDA/ROCm device supports dtype tf32."""
    if torch.version.hip:
        prop_name = torch.cuda.get_device_properties().gcnArchName
        archs = ("gfx94", "gfx95")
        for arch in archs:
            if arch in prop_name:
                return True
        return False

    # Otherwise, tf32 is supported on CUDA platforms that natively (i.e. no emulation)
    # support bfloat16.
    return is_bf16_supported(including_emulation=False)


def is_tf32_supported() -> bool:
    r"""Return a bool indicating if the current XPU device supports dtype tf32."""
    if not is_available():
        return False
    # On Intel Xe architecture and newer, TF32 operations can be accelerated
    # through DPAS (Dot Product Accumulate Systolic) instructions. Therefore,
    # TF32 support can be determined by checking whether the device supports
    # subgroup matrix multiply-accumulate operations.
    return torch.xpu.get_device_properties().has_subgroup_matrix_multiply_accumulate

