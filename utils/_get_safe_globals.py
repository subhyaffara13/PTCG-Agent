from typing import Callable

def _get_safe_globals() -> list[Callable | tuple[Callable, str]]:
    global _marked_safe_globals_set
    return list(_marked_safe_globals_set)

