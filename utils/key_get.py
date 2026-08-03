from typing import Any

def key_get(obj: Any, kp: KeyPath) -> Any:
    """Given an object and a key path, return the value at the key path."""
    raise NotImplementedError("KeyPaths are not yet supported in cxx_pytree.")


def key_get(obj: Any, kp: KeyPath) -> Any:
    """Given an object and a key path, return the value at the key path."""
    for k in kp:
        obj = k.get(obj)
    return obj

