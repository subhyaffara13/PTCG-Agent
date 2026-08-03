from typing import Any

def dtype_from_inputs(example_inputs: Iterable[Any]) -> torch.dtype:
    for x in example_inputs:
        if hasattr(x, "dtype"):
            return x.dtype
    return torch.float32  # Default fallback

