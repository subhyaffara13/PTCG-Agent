
def any_schema(
    *, ref: str | None = None, metadata: dict[str, Any] | None = None, serialization: SerSchema | None = None
) -> AnySchema:
    """
    Returns a schema that matches any value, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.any_schema()
    v = SchemaValidator(schema)
    assert v.validate_python(1) == 1
    ```

    Args:
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(type='any', ref=ref, metadata=metadata, serialization=serialization)

