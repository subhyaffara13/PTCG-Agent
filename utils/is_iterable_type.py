
def is_iterable_type(typ: type) -> bool:
    """If the given type is `typing.Iterable[T]`"""
    origin = get_origin(typ) or typ
    return origin == Iterable or origin == _c_abc.Iterable

