from typing import Any

def _all_elements_same(values: list[Any]) -> bool:
    if not values:
        return True
    first_value = values[0]
    return all(value == first_value for value in values)

