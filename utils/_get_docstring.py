from typing import Callable

def _get_docstring(plugin: Callable[..., T]) -> str:
    return inspect.getdoc(plugin) or ''

