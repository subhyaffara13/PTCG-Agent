from typing import Any

def none_schema(
    *, ref: str | None = None, metadata: dict[str, Any] | None = None, serialization: SerSchema | None = None
) -> NoneSchema:
    """
    Returns a schema that matches a None value, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.none_schema()
    v = SchemaValidator(schema)
    assert v.validate_python(None) is None
    ```

    Args:
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(type='none', ref=ref, metadata=metadata, serialization=serialization)

