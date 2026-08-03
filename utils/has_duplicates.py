from typing import Any

def has_duplicates(seq: Sequence[Any]) -> bool:
    return len(seq) > len(set(seq))

