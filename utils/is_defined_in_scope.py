
def is_defined_in_scope(
    var_node: nodes.NodeNG,
    varname: str,
    scope: nodes.NodeNG,
) -> bool:
    return defnode_in_scope(var_node, varname, scope) is not None

