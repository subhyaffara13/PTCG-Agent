from typing import Callable

def _disable_side_effect_safety_checks_for_current_subtracer(
    fn: Callable[_P, R], *args: _P.args, **kwargs: _P.kwargs
) -> R:
    return fn(*args, **kwargs)

