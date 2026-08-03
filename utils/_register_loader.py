from typing import Callable

def _register_loader(idx: int, size: int) -> Callable[[_LoaderFunc], _LoaderFunc]:
    def decorator(func: _LoaderFunc) -> _LoaderFunc:
        from .TiffTags import TYPES

        if func.__name__.startswith("load_"):
            TYPES[idx] = func.__name__[5:].replace("_", " ")
        _load_dispatch[idx] = size, func  # noqa: F821
        return func

    return decorator

