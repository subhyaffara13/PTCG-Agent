
def replace_nodes_in_symbol_table(
    symbols: SymbolTable, replacements: dict[SymbolNode, SymbolNode]
) -> None:
    for node in symbols.values():
        if node.node:
            if node.node in replacements:
                new = replacements[node.node]
                old = node.node
                replace_object_state(new, old, skip_slots=_get_ignored_slots(new))
                node._node = new
            if isinstance(node.node, (Var, TypeAlias)):
                # Handle them here just in case these aren't exposed through the AST.
                node.node.accept(NodeReplaceVisitor(replacements))

