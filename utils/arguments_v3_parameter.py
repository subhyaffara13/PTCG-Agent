
def arguments_v3_parameter(
    name: str,
    schema: CoreSchema,
    *,
    mode: Literal[
        'positional_only',
        'positional_or_keyword',
        'keyword_only',
        'var_args',
        'var_kwargs_uniform',
        'var_kwargs_unpacked_typed_dict',
    ]
    | None = None,
    alias: str | list[str | int] | list[list[str | int]] | None = None,
) -> ArgumentsV3Parameter:
    """
    Returns a schema that matches an argument parameter, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    param = core_schema.arguments_v3_parameter(
        name='a', schema=core_schema.str_schema(), mode='positional_only'
    )
    schema = core_schema.arguments_v3_schema([param])
    v = SchemaValidator(schema)
    assert v.validate_python({'a': 'hello'}) == (('hello',), {})
    ```

    Args:
        name: The name to use for the argument parameter
        schema: The schema to use for the argument parameter
        mode: The mode to use for the argument parameter
        alias: The alias to use for the argument parameter
    """
    return _dict_not_none(name=name, schema=schema, mode=mode, alias=alias)

