
def get_unpatched(item: _UnpatchT) -> _UnpatchT: ...


def get_unpatched(item: object) -> None: ...


def get_unpatched(
    item: type | types.FunctionType | object,
) -> type | types.FunctionType | None:
    if isinstance(item, type):
        return get_unpatched_class(item)
    if isinstance(item, types.FunctionType):
        return get_unpatched_function(item)
    return None

