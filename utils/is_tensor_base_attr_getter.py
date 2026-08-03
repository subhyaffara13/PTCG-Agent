from typing import Any

def is_tensor_base_attr_getter(value: Any) -> bool:
    return (
        isinstance(value, types.MethodWrapperType)
        and value.__name__ == "__get__"
        and hasattr(value.__self__, "__objclass__")
        and value.__self__.__objclass__ is torch._C._TensorBase  # type: ignore[attr-defined]
    )

