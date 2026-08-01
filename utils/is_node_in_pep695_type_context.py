
def is_node_in_pep695_type_context(node: nodes.NodeNG) -> nodes.NodeNG | None:
    """Check if node is used in a TypeAlias or as part of a type param."""
    return get_node_first_ancestor_of_type(
        node, (nodes.TypeAlias, nodes.TypeVar, nodes.ParamSpec, nodes.TypeVarTuple)
    )

