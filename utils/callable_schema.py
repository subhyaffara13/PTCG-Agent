
def callable_schema(
    *, ref: str | None = None, metadata: dict[str, Any] | None = None, serialization: SerSchema | None = None
) -> CallableSchema:
    """
    Returns a schema that checks if a value is callable, equivalent to python's `callable` method, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.callable_schema()
    v = SchemaValidator(schema)
    v.validate_python(min)
    ```

    Args:
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(type='callable', ref=ref, metadata=metadata, serialization=serialization)

