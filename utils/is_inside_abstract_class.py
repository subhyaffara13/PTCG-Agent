
def is_inside_abstract_class(node: nodes.NodeNG) -> bool:
    while node is not None:
        if isinstance(node, nodes.ClassDef):
            if class_is_abstract(node):
                return True
            name = getattr(node, "name", None)
            if name is not None and _is_abstract_class_name(name):
                return True
        node = node.parent
    return False

