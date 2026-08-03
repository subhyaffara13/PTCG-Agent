from typing import Any

def _no_mutation(self: Any, *args: Any, **kwargs: Any) -> NoReturn:
    raise TypeError(
        f"{type(self).__name__!r} object does not support mutation. {_help_mutation}",
    )

