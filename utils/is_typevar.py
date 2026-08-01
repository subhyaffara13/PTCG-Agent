
def is_typevar(typ: type) -> bool:
    # type ignore is required because type checkers
    # think this expression will always return False
    return type(typ) == TypeVar  # type: ignore

