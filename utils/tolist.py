from typing import Any

def tolist(x) -> list[Any]:
    if isinstance(x, list):
        return x
    elif hasattr(x, "numpy"):
        x = x.numpy()
    return x.tolist()

