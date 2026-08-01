
def _is_exempt_from_public_methods(node: nodes.ClassDef) -> bool:
    """Check if a class is exempt from too-few-public-methods."""
    # If it's a typing.Namedtuple, typing.TypedDict or an Enum
    for ancestor in node.ancestors():
        if is_enum(ancestor):
            return True
        if ancestor.qname() in (
            TYPING_NAMEDTUPLE,
            TYPING_TYPEDDICT,
            TYPING_EXTENSIONS_TYPEDDICT,
        ):
            return True

    # Or if it's a dataclass
    if not node.decorators:
        return False

    root_locals = set(node.root().locals)
    for decorator in node.decorators.nodes:
        if isinstance(decorator, nodes.Call):
            decorator = decorator.func
        match decorator:
            case nodes.Name(name=name) | nodes.Attribute(attrname=name):
                pass
            case _:
                continue
        if name in DATACLASSES_DECORATORS and (
            root_locals.intersection(DATACLASSES_DECORATORS)
            or DATACLASS_IMPORT in root_locals
        ):
            return True
        if name in ATTRS_DECORATORS and (
            root_locals.intersection(ATTRS_DECORATORS) or ATTRS_IMPORT in root_locals
        ):
            return True
    return False

