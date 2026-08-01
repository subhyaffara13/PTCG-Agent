
def snapshot_symbol_table(name_prefix: str, table: SymbolTable) -> dict[str, SymbolSnapshot]:
    """Create a snapshot description that represents the state of a symbol table.

    The snapshot has a representation based on nested tuples and dicts
    that makes it easy and fast to find differences.

    Only "shallow" state is included in the snapshot -- references to
    things defined in other modules are represented just by the names of
    the targets.
    """
    result: dict[str, SymbolSnapshot] = {}
    for name, symbol in table.items():
        node = symbol.node
        # TODO: cross_ref?
        fullname = node.fullname if node else None
        common = (fullname, symbol.kind, symbol.module_public)
        if isinstance(node, MypyFile):
            # This is a cross-reference to another module.
            # If the reference is busted because the other module is missing,
            # the node will be a "stale_info" TypeInfo produced by fixup,
            # but that doesn't really matter to us here.
            result[name] = ("Moduleref", common)
        elif isinstance(node, TypeVarExpr):
            result[name] = (
                "TypeVar",
                node.variance,
                [snapshot_type(value) for value in node.values],
                snapshot_type(node.upper_bound),
                snapshot_type(node.default),
            )
        elif isinstance(node, TypeAlias):
            result[name] = (
                "TypeAlias",
                snapshot_types(node.alias_tvars),
                node.normalized,
                node.no_args,
                snapshot_optional_type(node.target),
            )
        elif isinstance(node, ParamSpecExpr):
            result[name] = (
                "ParamSpec",
                node.variance,
                snapshot_type(node.upper_bound),
                snapshot_type(node.default),
            )
        elif isinstance(node, TypeVarTupleExpr):
            result[name] = (
                "TypeVarTuple",
                node.variance,
                snapshot_type(node.upper_bound),
                snapshot_type(node.default),
            )
        else:
            assert symbol.kind != UNBOUND_IMPORTED
            if node and get_prefix(node.fullname) != name_prefix:
                # This is a cross-reference to a node defined in another module.
                # Include the node kind (FuncDef, Decorator, TypeInfo, ...), so that we will
                # reprocess when a *new* node is created instead of merging an existing one.
                result[name] = ("CrossRef", common, type(node).__name__)
            else:
                result[name] = snapshot_definition(node, common)
    return result

