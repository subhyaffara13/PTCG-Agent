
def is_property_setter_or_deleter(node: nodes.NodeNG) -> bool:
    """Check if the given node is either a property setter or a deleter."""
    return _is_property_kind(node, "setter", "deleter")

