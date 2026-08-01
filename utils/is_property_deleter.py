
def is_property_deleter(node: nodes.NodeNG) -> bool:
    """Check if the given node is a property deleter."""
    return _is_property_kind(node, "deleter")

