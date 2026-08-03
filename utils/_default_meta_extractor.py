from typing import Any, Dict

def _default_meta_extractor(x: torch.Tensor) -> Dict[str, Any]:
    # These properties are fast to check, easy to understand
    return {
        "shape": x.shape,
        "dtype": x.dtype,
        "device": x.device
    }

