
def get_omitted_any(
    disallow_any: bool,
    fail: MsgCallback,
    note: MsgCallback,
    orig_type: Type,
    options: Options,
    fullname: str | None = None,
    unexpanded_type: Type | None = None,
    used_default: bool = False,
) -> AnyType:
    if disallow_any:
        typ = unexpanded_type or orig_type
        type_str = typ.name if isinstance(typ, UnboundType) else format_type_bare(typ, options)

        fail(
            message_registry.BARE_GENERIC.format(quote_type_string(type_str)),
            typ,
            code=codes.TYPE_ARG,
        )
        if used_default:
            note(message_registry.NO_CYCLIC_DEFAULT, typ, code=codes.TYPE_ARG)

        any_type = AnyType(TypeOfAny.from_error, line=typ.line, column=typ.column)
    else:
        any_type = AnyType(
            TypeOfAny.from_omitted_generics, line=orig_type.line, column=orig_type.column
        )
    return any_type

