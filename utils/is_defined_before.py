
def is_defined_before(var_node: nodes.Name) -> bool:
    """Check if the given variable node is defined before.

    Verify that the variable node is defined by a parent node
    (e.g. if or with) earlier than `var_node`, or is defined by a
    (list, set, dict, or generator comprehension, lambda)
    or in a previous sibling node on the same line
    (statement_defining ; statement_using).
    """
    varname = var_node.name
    for parent in var_node.node_ancestors():
        defnode = defnode_in_scope(var_node, varname, parent)
        if defnode is None:
            continue
        defnode_scope = defnode.scope()
        if isinstance(
            defnode_scope, (*COMP_NODE_TYPES, nodes.Lambda, nodes.FunctionDef)
        ):
            # Avoid the case where var_node_scope is a nested function
            if isinstance(defnode_scope, nodes.FunctionDef):
                var_node_scope = var_node.scope()
                if var_node_scope is not defnode_scope and isinstance(
                    var_node_scope, nodes.FunctionDef
                ):
                    return False
            return True
        if defnode.lineno < var_node.lineno:
            return True
        # `defnode` and `var_node` on the same line
        for defnode_anc in defnode.node_ancestors():
            if defnode_anc.lineno != var_node.lineno:
                continue
            if isinstance(
                defnode_anc,
                (
                    nodes.For,
                    nodes.While,
                    nodes.With,
                    nodes.Try,
                    nodes.ExceptHandler,
                ),
            ):
                return True
    # possibly multiple statements on the same line using semicolon separator
    stmt = var_node.statement()
    _node = stmt.previous_sibling()
    lineno = stmt.fromlineno
    while _node and _node.fromlineno == lineno:
        for assign_node in _node.nodes_of_class(nodes.AssignName):
            if assign_node.name == varname:
                return True
        for imp_node in _node.nodes_of_class((nodes.ImportFrom, nodes.Import)):
            if varname in [name[1] or name[0] for name in imp_node.names]:
                return True
        _node = _node.previous_sibling()
    return False

