from typing import Any

def get_function_dict(x: FuncIR) -> dict[str, Any]:
    """Get a dict of function attributes safe to compare across serialization"""
    d = get_dict(x)
    d.pop("blocks", None)
    d.pop("env", None)
    return d

