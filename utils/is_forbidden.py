from typing import Any

def is_forbidden(obj: Any) -> bool:
    _maybe_init_lazy_module(obj)
    return inspect.getattr_static(obj, "_dynamo_forbidden", False)

