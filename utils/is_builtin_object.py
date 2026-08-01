
def is_builtin_object(node: nodes.NodeNG) -> bool:
    """Returns True if the given node is an object from the __builtin__ module."""
    return node and node.root().name == "builtins"  # type: ignore[no-any-return]

