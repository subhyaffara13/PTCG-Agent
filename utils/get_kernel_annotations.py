from typing import Any

def get_kernel_annotations() -> dict[int, list[Any]]:
    """Return the current kernel annotation map (toolsId -> annotations)."""
    return _kernel_annotations

