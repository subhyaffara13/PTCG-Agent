
def _looks_like_typing_subscript(node) -> bool:
    """Try to figure out if a Subscript node *might* be a typing-related subscript."""
    if isinstance(node, nodes.Name):
        return node.name in TYPING_MEMBERS
    if isinstance(node, nodes.Attribute):
        return node.attrname in TYPING_MEMBERS
    if isinstance(node, nodes.Subscript):
        return _looks_like_typing_subscript(node.value)
    return False

