
def overrides_a_method(class_node: nodes.ClassDef, name: str) -> bool:
    """Return True if <name> is a method overridden from an ancestor
    which is not the base object class.
    """
    for ancestor in class_node.ancestors():
        if ancestor.name == "object":
            continue
        if name in ancestor and isinstance(ancestor[name], nodes.FunctionDef):
            return True
    return False

