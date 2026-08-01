
def _node_get(node: torch._C.Node, key: str):
    """Get attributes of a node which is polymorphic over return type."""
    sel = node.kindOf(key)
    return getattr(node, sel)(key)


def _node_get(node: _C.Node, key: str):
    """Gets attributes of a node which is polymorphic over return type."""
    if not isinstance(node, _C.Node):
        raise AssertionError(f"Expected _C.Node, got {type(node)}")
    sel = node.kindOf(key)
    return getattr(node, sel)(key)

