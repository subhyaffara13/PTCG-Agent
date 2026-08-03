from typing import Any

def is_ones(items: Sequence[Any]) -> bool:
    return all(x == 1 for x in items)

