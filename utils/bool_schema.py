from typing import Any

def bool_schema(
    strict: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> BoolSchema:
    """
    Returns a schema that matches a bool value, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.bool_schema()
    v = SchemaValidator(schema)
    assert v.validate_python('True') is True
    ```

    Args:
        strict: Whether the value should be a bool or a value that can be converted to a bool
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(type='bool', strict=strict, ref=ref, metadata=metadata, serialization=serialization)

