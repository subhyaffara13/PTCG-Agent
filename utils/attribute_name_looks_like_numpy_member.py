
def attribute_name_looks_like_numpy_member(
    member_names: frozenset[str], node: nodes.Attribute
) -> bool:
    """
    Returns True if the Attribute node's name matches a member name from numpy
    """
    return (
        node.attrname in member_names
        and isinstance(node.expr, nodes.Name)
        and _is_a_numpy_module(node.expr)
    )

