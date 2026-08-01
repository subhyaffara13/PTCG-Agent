
def _compile_start() -> None:
    global _t0, _triton_kernel_metrics
    if _t0 is None:
        _t0 = time()
    if _triton_kernel_metrics is None:
        _triton_kernel_metrics = {}

