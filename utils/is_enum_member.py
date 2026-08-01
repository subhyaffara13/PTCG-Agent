
def is_enum_member(node: nodes.AssignName) -> bool:
    """Return `True` if `node` is an Enum member (is an item of the
    `__members__` container).
    """
    frame = node.frame()
    if (
        not isinstance(frame, nodes.ClassDef)
        or not frame.is_subtype_of("enum.Enum")
        or frame.root().qname() == "enum"
    ):
        return False

    members = frame.locals.get("__members__")
    # A dataclass is one known case for when `members` can be `None`
    if members is None:
        return False
    return node.name in [name_obj.name for value, name_obj in members[0].items]

