
def complex_schema(
    *,
    strict: bool | None = None,
    ref: str | None = None,
    metadata: dict[str, Any] | None = None,
    serialization: SerSchema | None = None,
) -> ComplexSchema:
    """
    Returns a schema that matches a complex value, e.g.:

    ```py
    from pydantic_core import SchemaValidator, core_schema

    schema = core_schema.complex_schema()
    v = SchemaValidator(schema)
    assert v.validate_python('1+2j') == complex(1, 2)
    assert v.validate_python(complex(1, 2)) == complex(1, 2)
    ```

    Args:
        strict: Whether the value should be a complex object instance or a value that can be converted to a complex object
        ref: optional unique identifier of the schema, used to reference the schema in other places
        metadata: Any other information you want to include with the schema, not used by pydantic-core
        serialization: Custom serialization schema
    """
    return _dict_not_none(
        type='complex',
        strict=strict,
        ref=ref,
        metadata=metadata,
        serialization=serialization,
    )

