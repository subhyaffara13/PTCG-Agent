from typing import Any

def hashable(x: Any) -> bool:
    try:
        hash(x)
        return True
    except TypeError:
        return False
    # cannot hash writable memoryview object
    except ValueError:
        return False


def hashable(x):
    try:
        hash(x)
        return True
    except TypeError:
        return False

