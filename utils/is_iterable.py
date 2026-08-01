
def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def is_iterable(value: nodes.NodeNG, check_async: bool = False) -> bool:
    if check_async:
        protocol_check = _supports_async_iteration_protocol
    else:
        protocol_check = _supports_iteration_protocol
    return _supports_protocol(value, protocol_check)


def is_iterable(obj: object) -> TypeGuard[Iterable[object]]:
    return isinstance(obj, Iterable)

