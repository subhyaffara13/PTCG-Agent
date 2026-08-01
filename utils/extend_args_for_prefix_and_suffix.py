
def extend_args_for_prefix_and_suffix(
    types: tuple[Type, ...], prefix: int, suffix: int
) -> tuple[Type, ...]:
    """Extend list of types by eating out from variadic tuple to satisfy prefix and suffix."""
    idx = None
    item = None
    for i, t in enumerate(types):
        if isinstance(t, UnpackType):
            p_type = get_proper_type(t.type)
            if isinstance(p_type, Instance) and p_type.type.fullname == "builtins.tuple":
                item = p_type.args[0]
                idx = i
                break

    if idx is None:
        return types
    assert item is not None
    if idx < prefix:
        start = (item,) * (prefix - idx)
    else:
        start = ()
    if len(types) - idx - 1 < suffix:
        end = (item,) * (suffix - len(types) + idx + 1)
    else:
        end = ()
    return types[:idx] + start + (types[idx],) + end + types[idx + 1 :]

