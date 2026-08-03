from typing import Any

def fontInfoPostscriptWindowsCharacterSetValidator(value: Any) -> bool:
    """
    Version 2+.
    """
    validValues = list(range(1, 21))
    if value not in validValues:
        return False
    return True

