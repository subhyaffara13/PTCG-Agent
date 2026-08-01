
def _extract_underlying_field_name(typ: Type) -> str | None:
    """If the given type corresponds to some Enum instance, returns the
    original name of that enum. For example, if we receive in the type
    corresponding to 'SomeEnum.FOO', we return the string "SomeEnum.Foo".

    This helper takes advantage of the fact that Enum instances are valid
    to use inside Literal[...] types. An expression like 'SomeEnum.FOO' is
    actually represented by an Instance type with a Literal enum fallback.

    We can examine this Literal fallback to retrieve the string.
    """
    typ = get_proper_type(typ)
    if not isinstance(typ, Instance):
        return None

    if not typ.type.is_enum:
        return None

    underlying_literal = typ.last_known_value
    if underlying_literal is None:
        return None

    # The checks above have verified this LiteralType is representing an enum value,
    # which means the 'value' field is guaranteed to be the name of the enum field
    # as a string.
    assert isinstance(underlying_literal.value, str)
    return underlying_literal.value

