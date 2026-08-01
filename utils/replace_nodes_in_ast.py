
def replace_nodes_in_ast(
    node: SymbolNode, replacements: dict[SymbolNode, SymbolNode]
) -> SymbolNode:
    """Replace all references to replacement map keys within an AST node, recursively.

    Also replace the *identity* of any nodes that have replacements. Return the
    *replaced* version of the argument node (which may have a different identity, if
    it's included in the replacement map).
    """
    visitor = NodeReplaceVisitor(replacements)
    node.accept(visitor)
    return replacements.get(node, node)

