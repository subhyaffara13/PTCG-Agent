
def use_aten_gemm_kernels() -> bool:
    return not (
        config.max_autotune or config.max_autotune_gemm
    ) or _use_autotune_backend("ATEN")

