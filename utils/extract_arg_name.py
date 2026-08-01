
def extract_arg_name(typ: Type) -> str | None:
    if isinstance(typ, RawExpressionType) and typ.base_type_name == "builtins.str":
        return typ.literal_value  # type: ignore[return-value]
    elif isinstance(typ, UnboundType):
        if typ.name == "None":
            return None
        return typ.name
    return None  # Invalid, but let validation handle it

