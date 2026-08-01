
def is_subclass_of(child: nodes.ClassDef, parent: nodes.ClassDef) -> bool:
    """Check if first node is a subclass of second node.

    :param child: Node to check for subclass.
    :param parent: Node to check for superclass.
    :returns: True if child is derived from parent. False otherwise.
    """
    if not all(isinstance(node, nodes.ClassDef) for node in (child, parent)):
        return False

    for ancestor in child.ancestors():
        try:
            if astroid.helpers.is_subtype(ancestor, parent):
                return True
        except astroid.exceptions._NonDeducibleTypeHierarchy:
            continue
    return False

