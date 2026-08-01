
def defnode_in_scope(
    var_node: nodes.NodeNG,
    varname: str,
    scope: nodes.NodeNG,
) -> nodes.NodeNG | None:
    if isinstance(scope, nodes.If):
        for node in scope.body:
            if isinstance(node, nodes.Nonlocal) and varname in node.names:
                return node
            if isinstance(node, nodes.Assign):
                for target in node.targets:
                    if isinstance(target, nodes.AssignName) and target.name == varname:
                        return target
    elif isinstance(scope, (COMP_NODE_TYPES, nodes.For)):
        for ass_node in scope.nodes_of_class(nodes.AssignName):
            if ass_node.name == varname:
                return ass_node
    elif isinstance(scope, nodes.With):
        for expr, ids in scope.items:
            if expr.parent_of(var_node):
                break
            if ids and isinstance(ids, nodes.AssignName) and ids.name == varname:
                return ids
    elif isinstance(scope, (nodes.Lambda, nodes.FunctionDef)):
        if scope.args.is_argument(varname):
            # If the name is found inside a default value
            # of a function, then let the search continue
            # in the parent's tree.
            if scope.args.parent_of(var_node):
                try:
                    scope.args.default_value(varname)
                    scope = scope.parent
                    defnode = defnode_in_scope(var_node, varname, scope)
                except astroid.NoDefault:
                    pass
                else:
                    return defnode
            return scope
        if getattr(scope, "name", None) == varname:
            return scope
    elif isinstance(scope, nodes.ExceptHandler):
        if isinstance(scope.name, nodes.AssignName):
            ass_node = scope.name
            if ass_node.name == varname:
                return ass_node
    return None

