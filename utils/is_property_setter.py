
def is_property_setter(node: nodes.NodeNG) -> bool:
    """Check if the given node is a property setter."""
    return _is_property_kind(node, "setter")

