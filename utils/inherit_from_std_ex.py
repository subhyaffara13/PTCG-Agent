
def inherit_from_std_ex(node: nodes.NodeNG | astroid.Instance) -> bool:
    """Return whether the given class node is subclass of
    exceptions.Exception.
    """
    ancestors = node.ancestors() if hasattr(node, "ancestors") else []
    return any(
        ancestor.name in {"Exception", "BaseException"}
        and ancestor.root().name == EXCEPTIONS_MODULE
        for ancestor in itertools.chain([node], ancestors)
    )

