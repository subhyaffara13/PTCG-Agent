
def object_build_class(
    node: nodes.Module | nodes.ClassDef, member: type
) -> nodes.ClassDef:
    """create astroid for a living class object"""
    basenames = [base.__name__ for base in member.__bases__]
    return _base_class_object_build(node, member, basenames)

