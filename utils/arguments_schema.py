from typing import Any

def arguments_schema(
    arguments: list[ArgumentsParameter],
    *,
    validate_by_name: bool | None = None,
    validate_by_alias: bool | None = None,
    var_args_schema: CoreSchema | None = None,
    var_kwargs_mode: VarKwargsMode | None = None,
    var_kwargs_schema: CoreSchema | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> ArgumentsSchema:
    """
    Returns a schema that matches an arguments schema, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    param_a = core_schema.arguments_parameter(
        name='a', schema=core_schema.str_schema(), mode='positional_only'
    )
    param_b = core_schema.arguments_parameter(
        name='b', schema=core_schema.bool_schema(), mode='positional_only'
    )
    schema = core_schema.arguments_schema([param_a, param_b])
    v = SchemaValidator(schema)
    assert v.validate_python(('hello', True)) == (('hello', True), {})
    ```

    Args:
        arguments: The arguments to use for the arguments schema
        validate_by_name: Whether to populate by the parameter names, defaults to `False`.
        validate_by_alias: Whether to populate by the parameter aliases, defaults to `True`.
        var_args_schema: The variable args schema to use for the arguments schema
        var_kwargs_mode: The validation mode to use for variadic keyword arguments. If `'uniform'`, every value of the
            keyword arguments will be validated against the `var_kwargs_schema` schema. If `'unpacked-typed-dict'`,
            the `var_kwargs_schema` argument must be a [`typed_dict_schema`][pydantic_core.core_schema.typed_dict_schema]
        var_kwargs_schema: The variable kwargs schema to use for the arguments schema
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='arguments',
        arguments_schema=arguments,
        validate_by_name=validate_by_name,
        validate_by_alias=validate_by_alias,
        var_args_schema=var_args_schema,
        var_kwargs_mode=var_kwargs_mode,
        var_kwargs_schema=var_kwargs_schema,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

