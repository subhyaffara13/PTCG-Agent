from typing import Any

def is_callable_disallowed(obj: Any) -> bool:
    _maybe_init_lazy_module(obj)
    return id(obj) in _disallowed_callable_ids

