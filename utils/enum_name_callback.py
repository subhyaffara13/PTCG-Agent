
def enum_name_callback(ctx: mypy.plugin.AttributeContext) -> Type:
    """This plugin refines the 'name' attribute in enums to act as if
    they were declared to be final.

    For example, the expression 'MyEnum.FOO.name' normally is inferred
    to be of type 'str'.

    This plugin will instead make the inferred type be a 'str' where the
    last known value is 'Literal["FOO"]'. This means it would be legal to
    use 'MyEnum.FOO.name' in contexts that expect a Literal type, just like
    any other Final variable or attribute.

    This plugin assumes that the provided context is an attribute access
    matching one of the strings found in 'ENUM_NAME_ACCESS'.
    """
    enum_field_name = _extract_underlying_field_name(ctx.type)
    if enum_field_name is None:
        return ctx.default_attr_type
    else:
        str_type = ctx.api.named_generic_type("builtins.str", [])
        literal_type = LiteralType(enum_field_name, fallback=str_type)
        return str_type.copy_modified(last_known_value=literal_type)

