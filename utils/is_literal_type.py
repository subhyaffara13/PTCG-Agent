
def is_literal_type(typ: ProperType, fallback_fullname: str, value: LiteralValue) -> bool:
    """Check if this type is a LiteralType with the given fallback type and value."""
    if isinstance(typ, Instance) and typ.last_known_value:
        typ = typ.last_known_value
    return (
        isinstance(typ, LiteralType)
        and typ.fallback.type.fullname == fallback_fullname
        and typ.value == value
    )


def is_literal_type(type_: type[Any]) -> bool:
    return get_origin(type_) is Literal


def is_literal_type(type_: Type[Any]) -> bool:
    return Literal is not None and get_origin(type_) in LITERAL_TYPES


def is_literal_type(tp: Type[Any]) -> bool:
    return get_origin(tp) in _LITERAL_TYPES

