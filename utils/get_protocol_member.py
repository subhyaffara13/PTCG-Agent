
def get_protocol_member(
    left: Instance, original_left: Type, member: str, class_obj: bool, is_lvalue: bool = False
) -> Type | None:
    if member == "__call__" and class_obj:
        # Special case: class objects always have __call__ that is just the constructor.
        return mypy.typeops.type_object_type(left.type)

    if member == "__call__" and left.type.is_metaclass(precise=True):
        # Special case: we want to avoid falling back to metaclass __call__
        # if constructor signature didn't match, this can cause many false negatives.
        return None

    subtype = find_member(member, left, original_left, class_obj=class_obj, is_lvalue=is_lvalue)
    if isinstance(subtype, PartialType):
        subtype = (
            NoneType()
            if subtype.type is None
            else Instance(
                subtype.type, [AnyType(TypeOfAny.unannotated)] * len(subtype.type.type_vars)
            )
        )
    return subtype

