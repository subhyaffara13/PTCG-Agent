from typing import Any

def _validate_shrink_backend_requirements(group_info: dict) -> Any:
    """Return the backend implementation for the target group or raise if unsupported."""
    target_pg = group_info["process_group"]
    group_name = group_info["group_name"]

    # Get the group's backend directly via ProcessGroup API. Prefer a bound device if present,
    # otherwise try CUDA then fall back to CPU.
    try:
        preferred_device = getattr(target_pg, "bound_device_id", None)
        if preferred_device is not None:
            backend_impl = target_pg._get_backend(preferred_device)
        else:
            # Try CUDA first if available, else CPU
            try:
                backend_impl = target_pg._get_backend(torch.device("cuda"))
            except Exception:
                backend_impl = target_pg._get_backend(torch.device("cpu"))
    except RuntimeError as e:
        raise RuntimeError(
            f"Cannot access device backend for process group '{group_name}'. "
            f"Ensure the process group was initialized with a compatible device backend and devices are available."
        ) from e

    try:
        supports = bool(backend_impl.supports_shrinking)
    except Exception:
        supports = False
    if not supports:
        raise TypeError(
            f"Process group backend for '{group_name}' does not support shrinking operations."
        )

    return backend_impl

