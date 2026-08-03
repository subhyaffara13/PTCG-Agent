from typing import Any

def filter_none(values: Iterable[Any]) -> Any:
    """Filter out ``None`` from an iterable of values.

    >>> filter_none([1, 2, None, 3])  # doctest: +ELLIPSIS
    <filter object at 0x...>
    >>> list(filter_none([1, 2, None, 3]))
    [1, 2, 3]

    :param values: The optional values.
    :return: The filtered values.
    """
    return filter(partial(is_not, None), values)


def filter_none(obj: dict[str, Any]) -> dict[str, Any]: ...


def filter_none(obj: list[Any]) -> list[Any]: ...


def filter_none(obj: dict[str, Any] | list[Any]) -> dict[str, Any] | list[Any]:
    if isinstance(obj, dict):
        cleaned: dict[str, Any] = {}
        for k, v in obj.items():
            if v is None:
                continue
            if isinstance(v, (dict, list)):
                v = filter_none(v)
            cleaned[k] = v
        return cleaned

    if isinstance(obj, list):
        return [filter_none(v) if isinstance(v, (dict, list)) else v for v in obj]

    raise ValueError(f"Expected dict or list, got {type(obj)}")

