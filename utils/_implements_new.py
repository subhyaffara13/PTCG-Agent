
def _implements_new(info: TypeInfo) -> bool:
    """Check whether __new__ comes from enum.Enum or was implemented in a
    subclass of enum.Enum. In the latter case, we must infer Any as long as mypy can't infer
    the type of _value_ from assignments in __new__.

    If, however, __new__ comes from a user-defined class that is not an Enum subclass (i.e.
    the data type) this is allowed, because we should in general infer that an enum entry's
    value has that type.
    """
    type_with_new = _first(ti for ti in info.mro if ti.is_enum and ti.names.get("__new__"))
    if type_with_new is None:
        return False
    return type_with_new.fullname not in ("enum.Enum", "enum.IntEnum", "enum.StrEnum")

