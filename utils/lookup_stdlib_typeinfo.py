
def lookup_stdlib_typeinfo(fullname: str, modules: dict[str, MypyFile]) -> TypeInfo:
    """Find TypeInfo for a standard library type.

    This fast path assumes that the type exists at module top-level, use this
    function only for common types like `builtins.object` or `typing.Iterable`.
    """
    module, name = fullname.rsplit(".", maxsplit=1)
    sym = modules[module].names[name]
    assert isinstance(sym.node, TypeInfo)
    return sym.node

