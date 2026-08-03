from typing import Callable

def _unpickle_as_dead_weakref() -> Callable[[], None]:
    return lambda: None

