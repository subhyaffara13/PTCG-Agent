
def is_super(node: nodes.NodeNG) -> bool:
    """Return True if the node is referencing the "super" builtin function."""
    if getattr(node, "name", None) == "super" and node.root().name == "builtins":
        return True
    return False

