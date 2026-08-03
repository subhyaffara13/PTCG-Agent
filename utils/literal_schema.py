from typing import Any

def literal_schema(
    expected: list[Any],
    *,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> LiteralSchema:
    """
    Returns a schema that matches a literal value, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.literal_schema(['hello', 'world'])
    v = SchemaValidator(schema)
    assert v.validate_python('hello') == 'hello'
    ```

    Args:
        expected: The value must be one of these values
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(type='literal', expected=expected, ref=ref, metadata=metadata, serialization=serialization)

