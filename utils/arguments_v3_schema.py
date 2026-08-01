
def arguments_v3_schema(
    arguments: list[ArgumentsV3Parameter],
    *,
    validate_by_name: bool | None = None,
    validate_by_alias: bool | None = None,
    extra_behavior: Literal['forbid', 'ignore'] | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> ArgumentsV3Schema:
    """
    Returns a schema that matches an arguments schema, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    param_a = core_schema.arguments_v3_parameter(
        name='a', schema=core_schema.str_schema(), mode='positional_only'
    )
    param_b = core_schema.arguments_v3_parameter(
        name='kwargs', schema=core_schema.bool_schema(), mode='var_kwargs_uniform'
    )
    schema = core_schema.arguments_v3_schema([param_a, param_b])
    v = SchemaValidator(schema)
    assert v.validate_python({'a': 'hi', 'kwargs': {'b': True}}) == (('hi',), {'b': True})
    ```

    This schema is currently not used by other Pydantic components. In V3, it will most likely
    become the default arguments schema for the `'call'` schema.

    Args:
        arguments: The arguments to use for the arguments schema.
        validate_by_name: Whether to populate by the parameter names, defaults to `False`.
        validate_by_alias: Whether to populate by the parameter aliases, defaults to `True`.
        extra_behavior: The extra behavior to use.
        ref: optional unique identifier of the schema, used to reference the schema in other places.
        metadata: Any other information you want to include with the schema, not used by pydantic-core.
        serialization: Custom serialization schema.
    """
    return _dict_not_none(
        type='arguments-v3',
        arguments_schema=arguments,
        validate_by_name=validate_by_name,
        validate_by_alias=validate_by_alias,
        extra_behavior=extra_behavior,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

