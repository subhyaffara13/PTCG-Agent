from typing import Any

def _factory_args(fake_tensor: Tensor) -> dict[str, Any]:
    return {
        "device": fake_tensor.device,
        "dtype": fake_tensor.dtype,
    }

