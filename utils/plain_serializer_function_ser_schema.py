
def plain_serializer_function_ser_schema(
    function: SerializerFunction,
    *,
    is_field_serializer: bool | None = None,
    info_arg: bool | None = None,
    return_schema: CoreSchema | None = None,
    when_used: WhenUsed = 'always',
) -> PlainSerializerFunctionSerSchema:
    """
    Returns a schema for serialization with a function, can be either a "general" or "field" function.

    Args:
        function: The function to use for serialization
        is_field_serializer: Whether the serializer is for a field, e.g. takes `model` as the first argument,
            and `info` includes `field_name`
        info_arg: Whether the function takes an `info` argument
        return_schema: Schema to use for serializing return value
        when_used: When the function should be called
    """
    if when_used == 'always':
        # just to avoid extra elements in schema, and to use the actual default defined in rust
        when_used = None  # type: ignore
    return _dict_not_none(
        type='function-plain',
        function=function,
        is_field_serializer=is_field_serializer,
        info_arg=info_arg,
        return_schema=return_schema,
        when_used=when_used,
    )

