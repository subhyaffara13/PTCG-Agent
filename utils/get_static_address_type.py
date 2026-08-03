from typing import Any

def get_static_address_type(t: Any) -> Any:
    if isinstance(t, torch.Tensor):
        return getattr(t, "_dynamo_static_input_type", None)

    return None

