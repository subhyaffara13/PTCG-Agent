
def get_kernel_bin_format(device: str) -> str:
    if device == "cuda":
        return "cubin" if torch.version.hip is None else "hsaco"
    elif device == "xpu":
        return XPU_KERNEL_FORMAT
    else:
        return ""

