
def is_callable_type(type_: type[Any]) -> bool:
    return type_ is Callable or get_origin(type_) is Callable


def is_callable_type(type_hint) -> bool:  # type: ignore[no-untyped-def]
    """
    Special Case of is_type.
    """
    return type_hint.__name__ == "Callable"


def is_callable_type(type_: Type[Any]) -> bool:
    return type_ is Callable or get_origin(type_) is Callable

