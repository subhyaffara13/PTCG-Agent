from typing import Any, Callable

def _debug_get_cache_entry_list(
    code: types.CodeType | Callable[..., Any],
) -> list[CacheEntry]:
    """
    Given a code object or a callable object, retrieve the cache entries
     stored in this code.
    """
    if callable(code):
        code = code.__code__
    return torch._C._dynamo.eval_frame._debug_get_cache_entry_list(code)

