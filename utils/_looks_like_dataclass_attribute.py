
def _looks_like_dataclass_attribute(node: nodes.Unknown) -> bool:
    """Return True if node was dynamically generated as the child of an AnnAssign
    statement.
    """
    parent = node.parent
    if not parent:
        return False

    scope = parent.scope()
    return (
        isinstance(parent, nodes.AnnAssign)
        and isinstance(scope, nodes.ClassDef)
        and is_decorated_with_dataclass(scope)
    )

