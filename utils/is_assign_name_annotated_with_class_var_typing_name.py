
def is_assign_name_annotated_with_class_var_typing_name(
    node: nodes.AssignName, typing_name: str
) -> bool:
    if not is_assign_name_annotated_with(node, "ClassVar"):
        return False
    annotation = node.parent.annotation
    if isinstance(annotation, nodes.Subscript):
        annotation = annotation.slice
        if isinstance(annotation, nodes.Subscript):
            annotation = annotation.value
    match annotation:
        case nodes.Name(name=n) | nodes.Attribute(attrname=n) if n == typing_name:
            return True
    return False

