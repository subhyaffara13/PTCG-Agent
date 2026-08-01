
def get_outer_class(class_node: nodes.ClassDef) -> nodes.ClassDef | None:
    """Return the class that is the outer class of given (nested) class_node."""
    parent_klass = class_node.parent.frame()

    return parent_klass if isinstance(parent_klass, nodes.ClassDef) else None

