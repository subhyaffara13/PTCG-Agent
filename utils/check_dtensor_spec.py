from typing import Any

def check_dtensor_spec(value: Any, metadata: Any) -> bool:
    return value._check_equals(metadata, skip_shapes=True)

