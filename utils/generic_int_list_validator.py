from typing import Any

def genericIntListValidator(values: Any, validValues: Sequence[int]) -> bool:
    """
    Generic. (Added at version 2.)
    """
    if not isinstance(values, (list, tuple)):
        return False
    valuesSet = set(values)
    validValuesSet = set(validValues)
    if valuesSet - validValuesSet:
        return False
    for value in values:
        if not isinstance(value, int):
            return False
    return True

