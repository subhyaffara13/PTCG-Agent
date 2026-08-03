import functools
from typing import Any, Callable

def _copy_docstring_and_deprecators(
    method: Any,
    func: Literal[None] = None
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]: ...


def _copy_docstring_and_deprecators(
    method: Any, func: Callable[_P, _R]) -> Callable[_P, _R]: ...


def _copy_docstring_and_deprecators(
    method: Any,
    func: Callable[_P, _R] | None = None
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]] | Callable[_P, _R]:
    if func is None:
        return cast('Callable[[Callable[_P, _R]], Callable[_P, _R]]',
                    functools.partial(_copy_docstring_and_deprecators, method))
    decorators: list[Callable[[Callable[_P, _R]], Callable[_P, _R]]] = [
        _docstring.copy(method)
    ]
    # Check whether the definition of *method* includes @_api.rename_parameter
    # or @_api.make_keyword_only decorators; if so, propagate them to the
    # pyplot wrapper as well.
    while hasattr(method, "__wrapped__"):
        potential_decorator = _api.deprecation.DECORATORS.get(method)
        if potential_decorator:
            decorators.append(potential_decorator)
        method = method.__wrapped__
    for decorator in decorators[::-1]:
        func = decorator(func)
    _add_pyplot_note(func, method)
    return func

