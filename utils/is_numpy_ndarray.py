from typing import Any

def is_numpy_ndarray(value: Any) -> TypeGuard[np.ndarray]:  # type: ignore[type-arg]
    if not np:
        return False

    return istype(value, np.ndarray)

