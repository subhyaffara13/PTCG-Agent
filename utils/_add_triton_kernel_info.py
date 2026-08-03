from typing import Any

def _add_triton_kernel_info(kernel_name: str, info: dict[str, Any]):
    global _triton_kernel_metrics
    # Must be called between _compile_start and _compile_end
    if _triton_kernel_metrics is not None:
        _triton_kernel_metrics[kernel_name] = info

