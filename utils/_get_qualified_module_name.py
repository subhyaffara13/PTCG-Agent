from typing import Any

def _get_qualified_module_name(cls: Any) -> str:
    if isinstance(cls, str):
        return cls
    module = cls.__module__
    if module is None or module == str.__class__.__module__:
        return cls.__name__
    return module + "." + cls.__name__

