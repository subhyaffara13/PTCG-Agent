
def with_info_plain_validator_function(
    function: WithInfoValidatorFunction,
    *,
    field_name: str | None = None,
    ref: str | None = None,
    json_schema_input_schema: CoreSchema | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> PlainValidatorFunctionSchema:
    """
    Returns a schema that uses the provided function for validation, an `info` argument is passed, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    def fn(v: str, info: core_schema.ValidationInfo) -> str:
        assert 'hello' in v
        return v + 'world'

    schema = core_schema.with_info_plain_validator_function(function=fn)
    v = SchemaValidator(schema)
    assert v.validate_python('hello ') == 'hello world'
    ```

    Args:
        function: The validator function to call
        field_name: The name of the field this validator is applied to, if any (deprecated)
        ref: optional unique identifier of the schema, used to reference the schema in other places
        json_schema_input_schema: The core schema to be used to generate the corresponding JSON Schema input type
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    if field_name is not None:
        warnings.warn(
            'The `field_name` argument on `with_info_plain_validator_function` is deprecated, it will be passed to the function through `ValidationState` instead.',
            DeprecationWarning,
            stacklevel=2,
        )

    return _dict_not_none(
        type='function-plain',
        function=_dict_not_none(type='with-info', function=function, field_name=field_name),
        ref=ref,
        json_schema_input_schema=json_schema_input_schema,
        metadata=metadata,
        serialization=serialization,
    )

