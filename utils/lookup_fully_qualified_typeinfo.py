
def lookup_fully_qualified_typeinfo(
    modules: dict[str, MypyFile], name: str, *, allow_missing: bool
) -> TypeInfo:
    stnode = lookup_fully_qualified(name, modules, raise_on_missing=not allow_missing)
    node = stnode.node if stnode else None
    if isinstance(node, TypeInfo):
        return node
    else:
        # Looks like a missing TypeInfo during an initial daemon load, put something there
        assert (
            allow_missing
        ), "Should never get here in normal mode, got {}:{} instead of TypeInfo".format(
            type(node).__name__, node.fullname if node else ""
        )
        return missing_info(modules)

