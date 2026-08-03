from typing import Any

def _dict_unflatten(values: Iterable[T], context: Context) -> dict[Any, T]:
    return dict(zip(context, values, strict=True))

