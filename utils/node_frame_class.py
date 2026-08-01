
def node_frame_class(node: nodes.NodeNG) -> nodes.ClassDef | None:
    """Return the class that is wrapping the given node.

    The function returns a class for a method node (or a staticmethod or a
    classmethod), otherwise it returns `None`.
    """
    klass = node.frame()
    nodes_to_check = (
        nodes.NodeNG,
        astroid.UnboundMethod,
        astroid.BaseInstance,
    )
    while (
        klass
        and isinstance(klass, nodes_to_check)
        and not isinstance(klass, nodes.ClassDef)
    ):
        if klass.parent is None:
            return None

        klass = klass.parent.frame()

    return klass

