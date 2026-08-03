from typing import Any

def fontInfoOpenTypeOS2WeightClassValidator(value: Any) -> bool:
    """
    Version 2+.
    """
    if not isinstance(value, int):
        return False
    if value < 0:
        return False
    return True

