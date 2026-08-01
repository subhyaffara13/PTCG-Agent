
def json_or_python_schema(
    json_schema: CoreSchema,
    python_schema: CoreSchema,
    *,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> JsonOrPythonSchema:
    """
    Returns a schema that uses the Json or Python schema depending on the input:

    ```py
    from pydantic_core import SchemaValidator, ValidationError, core_schema

    v = SchemaValidator(
        core_schema.json_or_python_schema(
            json_schema=core_schema.int_schema(),
            python_schema=core_schema.int_schema(strict=True),
        )
    )

    assert v.validate_json('"123"') == 123

    try:
        v.validate_python('123')
    except ValidationError:
        pass
    else:
        raise AssertionError('Validation should have failed')
    ```

    Args:
        json_schema: The schema to use for Json inputs
        python_schema: The schema to use for Python inputs
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='json-or-python',
        json_schema=json_schema,
        python_schema=python_schema,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

