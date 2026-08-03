from typing import Callable

def copy_func_sig(
    source_func: Callable[_P, _R],
) -> Callable[[Callable[..., _R]], Callable[_P, _R]]:
    """Cast the decorated function's call signature and return type to the source_func's."""

    def _return(func: Callable[..., _R]) -> Callable[_P, _R]:
        return cast(Callable[_P, _R], func)

    return _return

