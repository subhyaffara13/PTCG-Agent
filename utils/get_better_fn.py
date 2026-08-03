from typing import Callable

def get_better_fn(key: str) -> Callable[[int, int, int, int], bool]:
    return _BETTER_FNS[key]

