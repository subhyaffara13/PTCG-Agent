import copy
from typing import Any

def _to_device_str(
    device: str,
    dtype: torch.dtype,
    non_blocking: bool = False,
    copy: bool = False,
    memory_format: torch.memory_format | None = None,
) -> dict[str, Any]:
    kwargs = {
        "device": torch.device(device),
        "dtype": dtype,
        "non_blocking": non_blocking,
        "copy": copy,
        "memory_format": memory_format,
    }
    return kwargs

