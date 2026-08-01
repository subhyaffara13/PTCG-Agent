
def class_is_abstract(node: nodes.ClassDef) -> bool:
    """Return true if the given class node should be considered as an abstract
    class.
    """
    # Protocol classes are considered "abstract"
    if is_protocol_class(node):
        return True

    # Only check for explicit metaclass=ABCMeta on this specific class
    meta = node.declared_metaclass()
    if meta is not None:
        if meta.name == "ABCMeta" and meta.root().name in ABC_MODULES:
            return True

    for ancestor in node.ancestors():
        if ancestor.name == "ABC" and ancestor.root().name in ABC_MODULES:
            # abc.ABC inheritance
            return True

    for method in node.methods():
        if method.parent.frame() is node:
            if method.is_abstract(pass_is_abstract=False):
                return True
    return False

