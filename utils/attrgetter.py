from typing import Any, Callable

def attrgetter(attr: str, /) -> Callable[[Any], _U]: ...


def attrgetter(
    attr1: str, attr2: str, /, *attrs: str
) -> Callable[[Any], tuple[_U1, _U2, Unpack[_Us]]]: ...


def attrgetter(*attrs: str) -> Callable[[Any], Any | tuple[Any, ...]]:
    if len(attrs) == 0:
        raise TypeError("attrgetter expected 1 argument, got 0")

    if any(not isinstance(attr, str) for attr in attrs):
        raise TypeError("attribute name must be a string")

    def resolve_attr(obj: Any, attr: str) -> Any:
        for name in attr.split("."):
            obj = getattr(obj, name)
        return obj

    if len(attrs) == 1:
        attr = attrs[0]

        def getter(obj: Any) -> Any:
            return resolve_attr(obj, attr)

    else:

        def getter(obj: Any) -> tuple[Any, ...]:  # type: ignore[misc]
            return tuple(resolve_attr(obj, attr) for attr in attrs)

    return getter

