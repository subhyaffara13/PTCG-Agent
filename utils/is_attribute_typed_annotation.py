
def is_attribute_typed_annotation(
    node: nodes.ClassDef | astroid.Instance, attr_name: str
) -> bool:
    """Test if attribute is typed annotation in current node
    or any base nodes.
    """
    match node.locals.get(attr_name, [None])[0]:
        case nodes.AssignName(parent=nodes.AnnAssign()):
            return True
    for base in node.bases:
        match inferred := safe_infer(base):
            case nodes.ClassDef() if is_attribute_typed_annotation(inferred, attr_name):
                return True
    return False

