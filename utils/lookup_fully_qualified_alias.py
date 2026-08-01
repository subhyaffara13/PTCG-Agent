
def lookup_fully_qualified_alias(
    modules: dict[str, MypyFile], name: str, *, allow_missing: bool
) -> TypeAlias:
    stnode = lookup_fully_qualified(name, modules, raise_on_missing=not allow_missing)
    node = stnode.node if stnode else None
    if isinstance(node, TypeAlias):
        return node
    elif isinstance(node, TypeInfo):
        if node.special_alias:
            # Already fixed up.
            return node.special_alias
        if node.tuple_type:
            alias = TypeAlias.from_tuple_type(node)
        elif node.typeddict_type:
            alias = TypeAlias.from_typeddict_type(node)
        else:
            assert allow_missing
            return missing_alias()
        node.special_alias = alias
        return alias
    else:
        # Looks like a missing TypeAlias during an initial daemon load, put something there
        assert (
            allow_missing
        ), "Should never get here in normal mode, got {}:{} instead of TypeAlias".format(
            type(node).__name__, node.fullname if node else ""
        )
        return missing_alias()

