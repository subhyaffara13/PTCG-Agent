import sys
from typing import Any

def _as_numpy_array(obj: object) -> ndarray | None:
    """
    Return an ndarray if the given object is implicitly convertible to ndarray,
    and numpy is already imported, otherwise None.
    """
    np: Any = sys.modules.get("numpy")
    if np is not None:
        # avoid infinite recursion on numpy scalars, which have __array__
        if np.isscalar(obj):
            return None
        elif isinstance(obj, np.ndarray):
            return obj
        elif hasattr(obj, "__array__") or hasattr(obj, "__array_interface__"):
            return np.asarray(obj)
    return None

