
def _promote_type_fft(
    dtype: torch.dtype, require_complex: bool, device: torch.device
) -> torch.dtype:
    """Helper to promote a dtype to one supported by the FFT primitives"""
    if dtype.is_complex:
        return dtype

    # Promote integral to default float type
    if not dtype.is_floating_point:
        dtype = torch.get_default_dtype()

    allowed_types = [torch.float32, torch.float64]
    maybe_support_half = device.type in ["cuda", "meta", "xpu"]

    if maybe_support_half:
        allowed_types.append(torch.float16)
    torch._check(dtype in allowed_types, lambda: f"Unsupported dtype {dtype}")

    if require_complex:
        dtype = utils.corresponding_complex_dtype(dtype)

    return dtype

