
def non_method_protocol_members(tp: TypeInfo) -> list[str]:
    """Find all non-callable members of a protocol."""

    assert tp.is_protocol
    result: list[str] = []
    anytype = AnyType(TypeOfAny.special_form)
    instance = Instance(tp, [anytype] * len(tp.defn.type_vars))

    for member in tp.protocol_members:
        typ = get_proper_type(find_member(member, instance, instance))
        if not isinstance(typ, (Overloaded, CallableType)):
            result.append(member)
    return result

