from typing import Any

def _prefix(value: Any) -> str:
    if isinstance(value, types.MethodType):
        name = describe(None, value.__self__, verbose=True) + "."
    else:
        module = inspect.getmodule(value)
        if module is not None and module.__name__ != "builtins":
            name = module.__name__ + "."
        else:
            name = ""
    return name

