
def get_quantize_fp8_per_row():
    if _is_torch_xpu_available:
        from .hub_kernels import get_kernel

        return get_kernel("kernels-community/fp8-fbgemm").quantize_fp8_per_row
    return torch.ops.fbgemm.quantize_fp8_per_row

