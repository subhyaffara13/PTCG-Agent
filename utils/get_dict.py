from typing import Any

def get_dict(x: Any) -> dict[str, Any]:
    if hasattr(x, "__mypyc_attrs__"):
        return {k: getattr(x, k) for k in x.__mypyc_attrs__ if hasattr(x, k)}
    else:
        return dict(x.__dict__)

