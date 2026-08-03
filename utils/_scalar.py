from typing import Any

def _scalar(x: torch.Tensor):
    """Convert a scalar tensor into a Python value."""
    if x.numel() != 1:
        raise AssertionError(f"Expected numel() == 1, got {x.numel()}")
    return x[0]


def _scalar(x: Any) -> Number | None:
    """Convert a scalar tensor into a Python value."""
    if isinstance(x, torch.Tensor) and x.shape == ():
        return x.item()
    return None

