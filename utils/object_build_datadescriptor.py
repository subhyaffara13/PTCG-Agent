
def object_build_datadescriptor(
    node: nodes.Module | nodes.ClassDef, member: type
) -> nodes.ClassDef:
    """create astroid for a living data descriptor object"""
    return _base_class_object_build(node, member, [])

