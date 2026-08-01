
def is_assign_name_annotated_with(node: nodes.AssignName, typing_name: str) -> bool:
    """Test if AssignName node has `typing_name` annotation.

    Especially useful to check for `typing._SpecialForm` instances
    like: `Union`, `Optional`, `Literal`, `ClassVar`, `Final`.
    """
    if not isinstance(node.parent, nodes.AnnAssign):
        return False
    annotation = node.parent.annotation
    if isinstance(annotation, nodes.Subscript):
        annotation = annotation.value
    match annotation:
        case nodes.Name(name=n) | nodes.Attribute(attrname=n) if n == typing_name:
            return True
    return False

