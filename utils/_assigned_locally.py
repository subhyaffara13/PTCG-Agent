
def _assigned_locally(name_node: nodes.Name) -> bool:
    """Checks if name_node has corresponding assign statement in same scope."""
    name_node_scope = name_node.scope()
    assign_stmts = name_node_scope.nodes_of_class(nodes.AssignName)
    return any(a.name == name_node.name for a in assign_stmts) or _find_frame_imports(
        name_node.name, name_node_scope
    )

