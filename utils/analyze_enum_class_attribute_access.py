
def analyze_enum_class_attribute_access(
    itype: Instance, name: str, mx: MemberContext
) -> Type | None:
    # Skip these since Enum will remove it
    if name in EXCLUDED_ENUM_ATTRIBUTES:
        return report_missing_attribute(mx.original_type, itype, name, mx)

    node = itype.type.get(name)
    if node and node.type:
        proper = get_proper_type(node.type)
        # Support `A = nonmember(1)` function call and decorator.
        if (
            isinstance(proper, Instance)
            and proper.type.fullname == "enum.nonmember"
            and proper.args
        ):
            return proper.args[0]

    if name not in itype.type.enum_members:
        return None

    enum_literal = LiteralType(name, fallback=itype)
    return itype.copy_modified(last_known_value=enum_literal)

