from typing import Any

def is_zeros(items: Sequence[Any]) -> bool:
    return all(x == 0 for x in items)

