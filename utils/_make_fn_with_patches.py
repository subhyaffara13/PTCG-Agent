import functools
from typing import Any, Callable

def _make_fn_with_patches(fn: Callable[_P, _T], *patches: Any) -> Callable[_P, _T]:
    @functools.wraps(fn)
    def _fn(*args: _P.args, **kwargs: _P.kwargs) -> _T:
        with contextlib.ExitStack() as stack:
            for module, attr, val in patches:
                stack.enter_context(patch.object(module, attr, val))

            return fn(*args, **kwargs)

    return _fn

