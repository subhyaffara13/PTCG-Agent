from typing import Any

def genericTypeValidator(value: Any, typ: Type[Any]) -> bool:
    """
    Generic. (Added at version 2.)
    """
    return isinstance(value, typ)

