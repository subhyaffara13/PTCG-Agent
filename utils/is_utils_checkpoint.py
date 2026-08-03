from typing import Any

def is_utils_checkpoint(obj: Any) -> bool:
    # Lazy import to avoid circular dependencies
    import torch.utils.checkpoint

    return obj is torch.utils.checkpoint.checkpoint

