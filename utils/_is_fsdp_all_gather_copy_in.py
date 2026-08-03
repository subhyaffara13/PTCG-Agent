from typing import Any

def _is_fsdp_all_gather_copy_in(func: Any) -> bool:
    """
    Check if func is torch.ops.fsdp.all_gather_copy_in.default by comparing
    namespace and name strings. This avoids accessing torch.ops.fsdp directly,
    which would fail on platforms where FSDP ops aren't registered (e.g., macOS
    builds with USE_DISTRIBUTED=0).
    """
    return (
        hasattr(func, "namespace")
        and func.namespace == "fsdp"
        and hasattr(func, "__name__")
        and func.__name__ == "all_gather_copy_in.default"
    )

