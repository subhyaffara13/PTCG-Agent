from typing import Callable

def copy_method_sig(
    source_method: Callable[Concatenate[_A1, _P], _R],
) -> Callable[[Callable[..., _R]], Callable[Concatenate[_A1, _P], _R]]:
    """Cast the decorated *method*'s call signature to the source_method and return type."""

    def _return(func: Callable[..., _R]) -> Callable[Concatenate[_A1, _P], _R]:
        return cast(Callable[Concatenate[_A1, _P], _R], func)

    return _return

