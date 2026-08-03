from typing import Any

def is_boolean_type(x: Any) -> TypeGuard[TensorBox | bool]:
    if isinstance(x, TensorBox):
        return is_boolean_dtype(x.get_dtype())
    else:
        return isinstance(x, bool)

