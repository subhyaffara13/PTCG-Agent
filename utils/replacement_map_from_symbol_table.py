
def replacement_map_from_symbol_table(
    old: SymbolTable, new: SymbolTable, prefix: str
) -> dict[SymbolNode, SymbolNode]:
    """Create a new-to-old object identity map by comparing two symbol table revisions.

    Both symbol tables must refer to revisions of the same module id. The symbol tables
    are compared recursively (recursing into nested class symbol tables), but only within
    the given module prefix. Don't recurse into other modules accessible through the symbol
    table.
    """
    replacements: dict[SymbolNode, SymbolNode] = {}
    for name, node in old.items():
        if name in new and (
            node.kind == MDEF or node.node and get_prefix(node.node.fullname) == prefix
        ):
            new_node = new[name]
            if (
                type(new_node.node) == type(node.node)
                and new_node.node
                and node.node
                and new_node.node.fullname == node.node.fullname
                and new_node.kind == node.kind
            ):
                replacements[new_node.node] = node.node
                if isinstance(node.node, TypeInfo) and isinstance(new_node.node, TypeInfo):
                    type_repl = replacement_map_from_symbol_table(
                        node.node.names, new_node.node.names, prefix
                    )
                    replacements.update(type_repl)
                    if node.node.special_alias and new_node.node.special_alias:
                        replacements[new_node.node.special_alias] = node.node.special_alias
    return replacements

