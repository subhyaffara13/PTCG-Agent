
def _looks_like_subscriptable(node: ClassDef) -> bool:
    """
    Returns True if the node corresponds to a ClassDef of the Collections.abc module
    that supports subscripting.

    :param node: ClassDef node
    """
    if node.qname().startswith("_collections") or node.qname().startswith(
        "collections"
    ):
        try:
            node.getattr("__class_getitem__")
            return True
        except AttributeInferenceError:
            pass
    return False

