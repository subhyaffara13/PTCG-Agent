from typing import Any

def device_from_inputs(example_inputs: Iterable[Any]) -> torch.device:
    for x in example_inputs:
        if hasattr(x, "device"):
            return x.device
    return torch.device("cpu")  # Default fallback

