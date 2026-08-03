from typing import Any

def urlopen(*args: Any, **kwargs: Any) -> Any:
    """
    Lazy-import wrapper for stdlib urlopen, as that imports a big chunk of
    the stdlib.
    """
    import urllib.request

    return urllib.request.urlopen(*args, **kwargs)  # noqa: TID251

