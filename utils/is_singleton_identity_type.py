
def is_singleton_identity_type(typ: ProperType) -> bool:
    """
    Returns True if every value of this type is identical to every other value of this type,
    as judged by the `is` operator.

    Note that this is not true of certain LiteralType, such as Literal[100001] or Literal["string"]
    """
    if isinstance(typ, NoneType):
        return True
    if isinstance(typ, Instance):
        return (
            (typ.type.is_enum and len(typ.type.enum_members) == 1)
            or (typ.type.fullname in ELLIPSIS_TYPE_NAMES)
            or (typ.type.fullname in NOT_IMPLEMENTED_TYPE_NAMES)
        )
    if isinstance(typ, LiteralType):
        return typ.is_enum_literal() or isinstance(typ.value, bool)
    if isinstance(typ, TypeType) and isinstance(typ.item, Instance) and typ.item.type.is_final:
        return True
    if isinstance(typ, FunctionLike) and typ.is_type_obj() and typ.type_object().is_final:
        return True
    return False

