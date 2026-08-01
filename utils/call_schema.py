
def call_schema(
    arguments: CoreSchema,
    function: Callable[..., Any],
    *,
    function_name: str | None = None,
    return_schema: CoreSchema | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> CallSchema:
    """
    Returns a schema that matches an arguments schema, then calls a function, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    param_a = core_schema.arguments_parameter(
        name='a', schema=core_schema.str_schema(), mode='positional_only'
    )
    param_b = core_schema.arguments_parameter(
        name='b', schema=core_schema.bool_schema(), mode='positional_only'
    )
    args_schema = core_schema.arguments_schema([param_a, param_b])

    schema = core_schema.call_schema(
        arguments=args_schema,
        function=lambda a, b: a + str(not b),
        return_schema=core_schema.str_schema(),
    )
    v = SchemaValidator(schema)
    assert v.validate_python((('hello', True))) == 'helloFalse'
    ```

    Args:
        arguments: The arguments to use for the arguments schema
        function: The function to use for the call schema
        function_name: The function name to use for the call schema, if not provided `function.__name__` is used
        return_schema: The return schema to use for the call schema
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='call',
        arguments_schema=arguments,
        function=function,
        function_name=function_name,
        return_schema=return_schema,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

