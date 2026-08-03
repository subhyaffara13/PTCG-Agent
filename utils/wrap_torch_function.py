import functools
from typing import Any, Callable

def wrap_torch_function(
    dispatcher: Callable[_P, Iterable[Any]],
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """Wraps a given function with ``__torch_function__`` -related functionality.

    Parameters
    ----------
    dispatcher: Callable
        A callable that returns an iterable of Tensor-likes passed into the function.

    Note
    ----
    This decorator may reduce the performance of your code. Generally, it's enough to express
    your code as a series of functions that, themselves, support __torch_function__. If you
    find yourself in the rare situation where this is not the case, e.g. if you're wrapping a
    low-level library and you also need it to work for Tensor-likes, then this function is available.

    Examples
    --------
    >>> def dispatcher(a):  # Must have the same signature as func
    ...     return (a,)
    >>> @torch.overrides.wrap_torch_function(dispatcher)
    >>> def func(a):  # This will make func dispatchable by __torch_function__
    ...     return a + 0
    """

    def inner(func: Callable[_P, _R]) -> Callable[_P, _R]:
        @functools.wraps(func)
        def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _R:
            relevant_args = dispatcher(*args, **kwargs)
            if has_torch_function(relevant_args):
                return handle_torch_function(
                    cast(Callable[_P, _R], wrapped), relevant_args, *args, **kwargs
                )

            return func(*args, **kwargs)

        return cast(Callable[_P, _R], wrapped)

    return inner

