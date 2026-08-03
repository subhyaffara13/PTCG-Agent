from typing import Callable

def flip_compat_check(is_compat: Callable[[Type, Type], bool]) -> Callable[[Type, Type], bool]:
    def new_is_compat(left: Type, right: Type) -> bool:
        return is_compat(right, left)

    return new_is_compat

